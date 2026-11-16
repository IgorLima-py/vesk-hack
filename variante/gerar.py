"""A variante de uma mudança só, sem perda fora do trecho mudado, e o certificado dela.

A mudança `marca_no_inicio` troca cada quadro do 1º segundo pelo quadro da marca (o primeiro quadro com pts >= o
segundo da marca). Todo o resto do vídeo passa igual: os quadros saem do decodificador em cru, no formato de pixel
do original, e voltam pelo x264 sem perda (`-qp 0`); o áudio é copiado sem recodificar. Assim cada quadro
decodificado fora do trecho é igual, byte a byte, ao do original, e a mesma entrada dá o mesmo arquivo.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from variante import quadros as q

VERSAO_CERTIFICADO = 1
MUDANCAS = ("marca_no_inicio",)
TRECHO_INICIO = 0.0
TRECHO_FIM = 1.0  # o trecho mudado é [0, 1 s)
ARQUIVO_VARIANTE = "variante.mp4"
ARQUIVO_CERTIFICADO = "certificado.json"

_OPCAO_DE_COR = {"color_space": "-colorspace", "color_primaries": "-color_primaries",
                 "color_transfer": "-color_trc", "color_range": "-color_range"}


def _numero(x: float) -> float | int:
    x = round(float(x), 6)
    return int(x) if x == int(x) else x


def gerar(video: Path, marca_em: float, mudanca: str, saida: Path) -> dict:
    if mudanca not in MUDANCAS:
        raise ValueError(f"mudança desconhecida {mudanca!r} (conheço: {', '.join(MUDANCAS)})")
    video = Path(video).resolve()
    saida = Path(saida)
    marca_em = float(marca_em)
    info = q.info(video)
    if marca_em < TRECHO_FIM:
        raise ValueError(f"a marca já está no 1º segundo ({marca_em:g} s); não há o que trazer para o início")
    if marca_em >= info.duracao:
        raise ValueError(f"--marca-em {marca_em:g} s passa do fim do vídeo ({info.duracao:g} s)")

    n_marca = q.primeiro_quadro_em(info, marca_em)
    quadro_fim = q.quadros_antes_de(info, TRECHO_FIM)
    ffmpeg = q.ferramenta("ffmpeg")

    # 1ª passada: só o quadro da marca, em cru.
    marca = None
    for n, quadro in enumerate(q.ler(video, info)):
        if n == n_marca:
            marca = quadro
            break
    if marca is None:
        raise q.VideoInvalido(f"o decodificador não chegou ao quadro {n_marca}")
    hash_marca = q.sha256(marca)

    # 2ª passada: o vídeo inteiro, com o trecho trocado, para o x264 sem perda.
    saida.mkdir(parents=True, exist_ok=True)
    parcial = saida / (ARQUIVO_VARIANTE + ".parcial.mp4")
    cmd = [ffmpeg, "-hide_banner", "-v", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", info.pix_fmt, "-s", f"{info.largura}x{info.altura}",
           "-framerate", f"{info.fps.numerator}/{info.fps.denominator}", "-i", "-",
           "-i", str(video), "-map", "0:v:0"]
    if info.tem_audio:
        cmd += ["-map", "1:a:0", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-qp", "0", "-preset", "medium", "-pix_fmt", info.pix_fmt]
    for chave, valor in info.cor.items():
        cmd += [_OPCAO_DE_COR[chave], valor]
    cmd += ["-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
            "-map_metadata", "-1", "-movflags", "+faststart", str(parcial)]

    fora: list[dict] = []
    with tempfile.TemporaryFile() as erro:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=erro)
        try:
            for n, quadro in enumerate(q.ler(video, info)):
                if n < quadro_fim:
                    proc.stdin.write(marca)
                else:
                    fora.append({"n": n, "hash": q.sha256(quadro)})
                    proc.stdin.write(quadro)
        except BrokenPipeError:
            pass
        finally:
            proc.stdin.close()
            proc.wait()
        if proc.returncode != 0:
            erro.seek(0)
            parcial.unlink(missing_ok=True)
            raise RuntimeError(f"o ffmpeg falhou ao gravar a variante ({proc.returncode}): "
                               f"{erro.read().decode('utf-8', 'replace')[-1500:]}")
    if len(fora) + quadro_fim != info.quadros:
        parcial.unlink(missing_ok=True)
        raise RuntimeError(f"o decodificador deu {len(fora) + quadro_fim} quadros, e o ffprobe {info.quadros}")

    destino = saida / ARQUIVO_VARIANTE
    parcial.replace(destino)

    certificado = {
        "versao": VERSAO_CERTIFICADO,
        "mudanca": mudanca,
        "original": {
            "caminho": str(video),
            "sha256": q.sha256_do_arquivo(video),
            "quadros": info.quadros,
            "largura": info.largura,
            "altura": info.altura,
            "fps": f"{info.fps.numerator}/{info.fps.denominator}",
            "pix_fmt": info.pix_fmt,
            "duracao": _numero(info.duracao),
        },
        "marca_em": _numero(marca_em),
        "quadro_da_marca": {"n": n_marca, "pts": _numero(info.pts[n_marca]), "hash": hash_marca},
        "trecho": {"inicio": _numero(TRECHO_INICIO), "fim": _numero(TRECHO_FIM),
                   "quadro_inicio": 0, "quadro_fim": quadro_fim},
        "hash_dos_quadros": "sha256 do quadro decodificado em cru, no pix_fmt do original",
        "fora": fora,
        "variante": {"arquivo": ARQUIVO_VARIANTE, "sha256": q.sha256_do_arquivo(destino)},
        "ffmpeg": q.versao_ffmpeg(),
    }
    (saida / ARQUIVO_CERTIFICADO).write_text(json.dumps(certificado, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
    return certificado
