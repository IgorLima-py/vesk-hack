"""O ffmpeg e o ffprobe: o que o vídeo é, e os quadros dele em cru, um por vez."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterator

# Os formatos de pixel que o x264 grava sem perda. O tamanho do quadro em cru sai da conta de cada um.
CROMA = {  # nome: (divisor da largura do croma, divisor da altura do croma)
    "yuv420p": (2, 2), "yuvj420p": (2, 2),
    "yuv422p": (2, 1), "yuvj422p": (2, 1),
    "yuv444p": (1, 1), "yuvj444p": (1, 1),
}
TOLERANCIA_PTS = 1e-4  # o ffprobe imprime o tempo com 6 casas


class FaltaFerramenta(RuntimeError):
    pass


class VideoInvalido(ValueError):
    pass


def ferramenta(nome: str) -> str:
    caminho = shutil.which(nome)
    if not caminho:
        raise FaltaFerramenta(f"{nome} não encontrado no PATH")
    return caminho


def versao_ffmpeg() -> str:
    saida = subprocess.run([ferramenta("ffmpeg"), "-hide_banner", "-version"], capture_output=True, text=True).stdout
    return saida.splitlines()[0] if saida else "desconhecida"


def sha256_do_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def sha256(dados: bytes) -> str:
    return hashlib.sha256(dados).hexdigest()


@dataclass(frozen=True)
class Info:
    largura: int
    altura: int
    pix_fmt: str
    fps: Fraction
    pts: tuple[float, ...]
    tem_audio: bool
    cor: dict[str, str]

    @property
    def quadros(self) -> int:
        return len(self.pts)

    @property
    def duracao(self) -> float:
        """A duração do vídeo: o pts do último quadro mais um quadro."""
        return self.pts[-1] + 1 / float(self.fps)

    @property
    def tamanho_do_quadro(self) -> int:
        dx, dy = CROMA[self.pix_fmt]
        cx, cy = -(-self.largura // dx), -(-self.altura // dy)
        return self.largura * self.altura + 2 * cx * cy


def _ffprobe_json(video: Path, *args: str) -> dict:
    feito = subprocess.run([ferramenta("ffprobe"), "-v", "error", *args, "-of", "json", str(video)],
                           capture_output=True, text=True)
    if feito.returncode != 0:
        raise VideoInvalido(f"o ffprobe não leu {video}: {feito.stderr.strip()[-500:]}")
    return json.loads(feito.stdout)


def info(video: Path) -> Info:
    """O que o vídeo é, com o pts de cada quadro decodificado. Recusa o que não dá para refazer sem perda."""
    video = Path(video)
    if not video.is_file():
        raise VideoInvalido(f"não achei o vídeo {video}")
    dados = _ffprobe_json(video, "-show_entries",
                          "stream=codec_type,width,height,pix_fmt,r_frame_rate,sample_aspect_ratio,"
                          "color_space,color_primaries,color_transfer,color_range")
    videos = [s for s in dados.get("streams", []) if s.get("codec_type") == "video"]
    if not videos:
        raise VideoInvalido(f"{video} não tem faixa de vídeo")
    v = videos[0]
    pix_fmt = v.get("pix_fmt", "")
    if pix_fmt not in CROMA:
        raise VideoInvalido(f"formato de pixel {pix_fmt!r} não suportado (aceito: {', '.join(CROMA)})")
    sar = v.get("sample_aspect_ratio", "1:1")
    if sar not in ("1:1", "0:1", "N/A"):
        raise VideoInvalido(f"pixel não quadrado (SAR {sar}) não suportado")
    fps = Fraction(v["r_frame_rate"])
    if fps <= 0:
        raise VideoInvalido(f"taxa de quadros inválida: {v['r_frame_rate']}")

    quadros = _ffprobe_json(video, "-select_streams", "v:0", "-show_entries", "frame=best_effort_timestamp_time")
    pts = tuple(float(q["best_effort_timestamp_time"]) for q in quadros.get("frames", []))
    if not pts:
        raise VideoInvalido(f"{video} não tem quadros")
    passo = 1 / float(fps)
    for i in range(1, len(pts)):
        if abs(pts[i] - pts[i - 1] - passo) > TOLERANCIA_PTS:
            raise VideoInvalido(
                f"taxa de quadros variável (entre o quadro {i - 1} e o {i}, {pts[i] - pts[i - 1]:.6f} s "
                f"em vez de {passo:.6f} s); só vídeo de taxa constante tem variante sem perda")

    cor = {chave: v[chave] for chave in ("color_space", "color_primaries", "color_transfer", "color_range")
           if v.get(chave) and v[chave] != "unknown"}
    tem_audio = any(s.get("codec_type") == "audio" for s in dados.get("streams", []))
    return Info(int(v["width"]), int(v["height"]), pix_fmt, fps, pts, tem_audio, cor)


def primeiro_quadro_em(i: Info, segundo: float) -> int:
    """O índice do primeiro quadro com pts >= segundo (o mesmo quadro que o `-ss` do ffmpeg acha)."""
    for n, t in enumerate(i.pts):
        if t >= segundo - TOLERANCIA_PTS:
            return n
    raise VideoInvalido(f"nenhum quadro em {segundo:g} s ou depois (o vídeo tem {i.duracao:g} s)")


def quadros_antes_de(i: Info, segundo: float) -> int:
    """Quantos quadros têm pts < segundo."""
    return sum(1 for t in i.pts if t < segundo - TOLERANCIA_PTS)


def ler(video: Path, i: Info) -> Iterator[bytes]:
    """Os quadros decodificados, em cru, no formato de pixel do próprio vídeo (sem conversão), um por vez."""
    erro = tempfile.TemporaryFile()
    proc = subprocess.Popen([ferramenta("ffmpeg"), "-v", "error", "-i", str(video), "-map", "0:v:0",
                             "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", i.pix_fmt, "-"],
                            stdout=subprocess.PIPE, stderr=erro)
    tamanho = i.tamanho_do_quadro
    terminou = False
    try:
        while True:
            quadro = proc.stdout.read(tamanho)
            if not quadro:
                break
            if len(quadro) != tamanho:
                raise VideoInvalido(f"quadro incompleto ao decodificar {video} ({len(quadro)} de {tamanho} bytes)")
            yield quadro
        terminou = True
    finally:
        if not terminou and proc.poll() is None:
            proc.kill()
        proc.stdout.close()
        proc.wait()
        erro.seek(0)
        mensagem = erro.read().decode("utf-8", "replace").strip()
        erro.close()
        if terminou and proc.returncode != 0:
            raise RuntimeError(f"o ffmpeg falhou ao decodificar {video} ({proc.returncode}): {mensagem[-1000:]}")


def hash_do_audio(video: Path) -> str | None:
    """O sha256 do áudio decodificado (PCM float), ou None se o vídeo não tem áudio."""
    dados = _ffprobe_json(video, "-show_entries", "stream=codec_type")
    if not any(s.get("codec_type") == "audio" for s in dados.get("streams", [])):
        return None
    proc = subprocess.Popen([ferramenta("ffmpeg"), "-v", "error", "-i", str(video), "-map", "0:a:0",
                             "-f", "f32le", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    h = hashlib.sha256()
    for bloco in iter(lambda: proc.stdout.read(1 << 20), b""):
        h.update(bloco)
    proc.stdout.close()
    if proc.wait() != 0:
        raise RuntimeError(f"o ffmpeg falhou ao decodificar o áudio de {video}")
    return h.hexdigest()
