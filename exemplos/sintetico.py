"""Gera um vídeo sintético com a resposta conhecida e o gabarito.json ao lado.

    python -m exemplos.sintetico --marca-em <s> --semente <n> --saida <mp4>
        [--duracao 15] [--sem-fala] [--sem-marca]

O vídeo tem cortes em segundos conhecidos (planos de cor lisa), o texto «VESK» em
magenta puro a partir do segundo da marca, e a frase «Vesk. The creative autopilot.»
na voz, começando no mesmo segundo. A voz vem do filtro `flite` do ffmpeg, que roda
sem rede (fonte em exemplos/README.md). A mesma semente dá o mesmo arquivo, byte a
byte, na mesma máquina e na mesma versão do ffmpeg.
"""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import random
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

VERSAO_GABARITO = 1
LARGURA, ALTURA, FPS = 720, 1280, 30
COR_DO_TEXTO = (255, 0, 255)
TEXTO_NA_TELA = "VESK"
TAMANHO_DA_FONTE = 160
FRASE_DA_MARCA = "Vesk. The creative autopilot."
FRASE_SEM_MARCA = "Watch this."
INICIO_DA_FRASE_SEM_MARCA = 0.5
VOZ = "kal16"
TAXA_DA_VOZ = 16000
LIMIAR_DA_VOZ = 500  # amplitude int16 (cerca de -36 dBFS) que conta como fala
TRECHOS = (1.5, 2.0, 2.5, 3.0, 3.5)  # duração de cada plano, em segundos
DURACAO_PADRAO = 15.0

# Paleta alternada: planos escuros (luma ~20-60) e claros (luma ~170-225), nenhum
# perto do magenta. Dois planos vizinhos diferem em mais de 100 de luma, e o
# `scene` do ffmpeg fica bem acima de 0,3 em cada corte.
ESCUROS = ((20, 30, 60), (30, 50, 30), (50, 40, 30), (25, 25, 25), (10, 50, 60), (60, 30, 20))
CLAROS = ((230, 220, 180), (200, 230, 200), (210, 210, 210), (180, 220, 240), (240, 200, 150), (220, 230, 140))


class FaltaFerramenta(RuntimeError):
    pass


def _ffmpeg() -> str:
    caminho = shutil.which("ffmpeg")
    if not caminho:
        raise FaltaFerramenta("ffmpeg não encontrado no PATH (precisa de um build com o filtro flite)")
    filtros = subprocess.run([caminho, "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    if not any(linha.split()[1:2] == ["flite"] for linha in filtros.splitlines()):
        raise FaltaFerramenta(
            "este ffmpeg não tem o filtro flite (TTS sem rede); use o build full do gyan.dev no Windows "
            "ou o pacote ffmpeg do Ubuntu"
        )
    return caminho


def _rodar(cmd: list[str]) -> None:
    feito = subprocess.run(cmd, capture_output=True, text=True)
    if feito.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou ({feito.returncode}): {feito.stderr[-2000:]}")


def _numero(x: float) -> float | int:
    """Inteiro quando o valor é inteiro, para o gabarito ficar legível."""
    x = round(float(x), 3)
    return int(x) if x == int(x) else x


def sortear_planos(rng: random.Random, duracao: float) -> tuple[list[float], list[tuple[int, int, int]]]:
    """Os cortes (segundos) e a cor de cada plano."""
    cortes: list[float] = []
    t = 0.0
    while True:
        t += rng.choice(TRECHOS)
        if t > duracao - 1.0:  # o último plano tem pelo menos 1 s
            break
        cortes.append(t)
    escuro = rng.random() < 0.5
    cores = []
    for _ in range(len(cortes) + 1):
        cores.append(rng.choice(ESCUROS if escuro else CLAROS))
        escuro = not escuro
    return cortes, cores


def _png_do_texto(caminho: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    fonte = ImageFont.load_default(size=TAMANHO_DA_FONTE)
    imagem = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    desenho = ImageDraw.Draw(imagem)
    x0, y0, x1, y1 = desenho.textbbox((0, 0), TEXTO_NA_TELA, font=fonte)
    x = (LARGURA - (x1 - x0)) // 2 - x0
    y = int(ALTURA * 0.62) - y0
    desenho.text((x, y), TEXTO_NA_TELA, font=fonte, fill=COR_DO_TEXTO + (255,))
    imagem.save(caminho)


def _voz(ffmpeg: str, frase: str, caminho: Path) -> array.array:
    _rodar([ffmpeg, "-hide_banner", "-y", "-f", "lavfi", "-i", f"flite=text='{frase}':voice={VOZ}",
            "-ar", str(TAXA_DA_VOZ), "-ac", "1", "-c:a", "pcm_s16le", str(caminho)])
    with wave.open(str(caminho), "rb") as w:
        amostras = array.array("h", w.readframes(w.getnframes()))
    if sys.byteorder == "big":
        amostras.byteswap()
    return amostras


def _limites(amostras: array.array) -> tuple[int, int]:
    """Primeira e última amostra acima do limiar."""
    acima = [i for i, a in enumerate(amostras) if abs(a) > LIMIAR_DA_VOZ]
    if not acima:
        raise RuntimeError("o flite devolveu silêncio")
    return acima[0], acima[-1] + 1


def gerar(marca_em: float, semente: int, saida: Path, duracao: float = DURACAO_PADRAO,
          fala: bool = True, marca: bool = True) -> dict:
    duracao = float(duracao)
    marca_em = float(marca_em)
    if duracao < 3:
        raise ValueError("--duracao precisa ser pelo menos 3 s")
    if not 0.5 <= marca_em <= duracao - 1:
        raise ValueError(f"--marca-em precisa estar entre 0,5 e {duracao - 1:g} s (duração {duracao:g} s)")

    ffmpeg = _ffmpeg()
    saida = Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(semente)
    cortes, cores = sortear_planos(rng, duracao)

    total = int(round(duracao * TAXA_DA_VOZ))
    faixa = array.array("h", bytes(2 * total))
    falas: list[dict] = []

    with tempfile.TemporaryDirectory(prefix="sintetico-") as tmp:
        tmp = Path(tmp)

        def por(frase: str, inicio: float, tem_marca: bool, nome: str) -> None:
            amostras = _voz(ffmpeg, frase, tmp / nome)
            a, b = _limites(amostras)
            base = int(round(inicio * TAXA_DA_VOZ)) - a  # o começo da fala cai em `inicio`
            fim = min(total, base + b)
            for i in range(max(0, base + a), fim):
                faixa[i] = amostras[i - base]
            falas.append({"texto": frase, "inicio": _numero(inicio),
                          "fim": _numero(fim / TAXA_DA_VOZ), "tem_marca": tem_marca})

        if fala:
            if marca:
                antes = _voz(ffmpeg, FRASE_SEM_MARCA, tmp / "antes.wav")
                a, b = _limites(antes)
                if INICIO_DA_FRASE_SEM_MARCA + (b - a) / TAXA_DA_VOZ + 0.5 <= marca_em:
                    por(FRASE_SEM_MARCA, INICIO_DA_FRASE_SEM_MARCA, False, "antes.wav")
                por(FRASE_DA_MARCA, marca_em, True, "marca.wav")
            else:
                por(FRASE_SEM_MARCA, INICIO_DA_FRASE_SEM_MARCA, False, "antes.wav")

        audio = tmp / "audio.wav"
        with wave.open(str(audio), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(TAXA_DA_VOZ)
            dados = array.array("h", faixa)
            if sys.byteorder == "big":
                dados.byteswap()
            w.writeframes(dados.tobytes())

        texto_png = tmp / "texto.png"
        _png_do_texto(texto_png)

        limites = [0.0] + cortes + [duracao]
        grafo = []
        for i, cor in enumerate(cores):
            d = limites[i + 1] - limites[i]
            grafo.append(f"color=c=0x{cor[0]:02x}{cor[1]:02x}{cor[2]:02x}:s={LARGURA}x{ALTURA}:r={FPS}:d={d:g}[p{i}]")
        grafo.append("".join(f"[p{i}]" for i in range(len(cores))) + f"concat=n={len(cores)}:v=1:a=0,format=rgb24[fundo]")
        if marca:
            grafo.append(f"[fundo][0:v]overlay=x=0:y=0:format=rgb:enable='gte(t,{marca_em:g})',format=yuv420p[v]")
        else:
            grafo.append("[fundo]format=yuv420p[v]")

        _rodar([
            ffmpeg, "-hide_banner", "-y",
            "-i", str(texto_png), "-i", str(audio),
            "-filter_complex", ";".join(grafo),
            "-map", "[v]", "-map", "1:a",
            "-t", f"{duracao:g}", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-colorspace", "smpte170m", "-color_primaries", "smpte170m", "-color_trc", "smpte170m",
            "-color_range", "tv",
            "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "1",
            "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
            "-map_metadata", "-1", "-movflags", "+faststart",
            str(saida),
        ])

    gabarito = {
        "versao": VERSAO_GABARITO,
        "semente": semente,
        "duracao": _numero(duracao),
        "fps": FPS,
        "largura": LARGURA,
        "altura": ALTURA,
        "marca_em": _numero(marca_em) if marca else None,
        "cortes": [_numero(c) for c in cortes],
        "fala": falas,
        "texto": [{"texto": TEXTO_NA_TELA, "inicio": _numero(marca_em), "fim": _numero(duracao)}] if marca else [],
        "cor_do_texto": list(COR_DO_TEXTO),
        "video_sha256": hashlib.sha256(saida.read_bytes()).hexdigest(),
    }
    (saida.parent / "gabarito.json").write_text(json.dumps(gabarito, ensure_ascii=False, indent=2) + "\n",
                                                encoding="utf-8")
    return gabarito


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m exemplos.sintetico", description=__doc__.split("\n")[0])
    p.add_argument("--marca-em", type=float, required=True, help="segundo em que a marca entra (texto e voz)")
    p.add_argument("--semente", type=int, required=True, help="sorteia os cortes e as cores")
    p.add_argument("--saida", type=Path, required=True, help="o .mp4; o gabarito.json vai na mesma pasta")
    p.add_argument("--duracao", type=float, default=DURACAO_PADRAO, help="em segundos (padrão 15)")
    p.add_argument("--sem-fala", action="store_true", help="áudio em silêncio")
    p.add_argument("--sem-marca", action="store_true", help="sem o texto e sem a frase da marca")
    a = p.parse_args(argv)
    try:
        g = gerar(a.marca_em, a.semente, a.saida, a.duracao, fala=not a.sem_fala, marca=not a.sem_marca)
    except (FaltaFerramenta, ValueError) as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    print(f"{a.saida} (marca_em={g['marca_em']}, cortes={g['cortes']}, sha256={g['video_sha256'][:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
