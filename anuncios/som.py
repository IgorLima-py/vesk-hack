"""O áudio de um anúncio ($VIDEOS/montagem/<a|b>/som.wav): cada fala no quadro dela e o logo sonoro na cartela.

A mistura é soma de inteiros, em Python, e por isso dá o mesmo arquivo toda vez. O logo sonoro sai do `aevalsrc` do
ffmpeg e entra com o mesmo pico da fala mais alta. No fim, o pico da mistura vai a `pico_dbfs`, sem loudnorm.
"""

from __future__ import annotations

import array
import hashlib
import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

from anuncios.caminhos import BRUTOS, BRUTOS_JSON, LINHA, MONTAGEM, parametros

# Escolha de desenho: duas notas senoidais, lá5 (880 Hz) e mi6 (1318,51 Hz, a quinta acima), a segunda entrando em
# 0,12 s; cada uma com 4 ms de ataque e queda exponencial, e 20 ms de saída no fim para não estalar.
LOGO = ("(sin(2*PI*880*t)*min(t/0.004,1)*exp(-12*t)"
        "+gte(t,0.12)*sin(2*PI*1318.51*(t-0.12))*min((t-0.12)/0.004,1)*exp(-6*(t-0.12)))"
        "*min(({d}-t)/0.02,1)")


def _ffmpeg() -> str:
    caminho = shutil.which("ffmpeg")
    if not caminho:
        raise SystemExit("ffmpeg não encontrado no PATH")
    return caminho


def _ler_wav(caminho: Path, taxa: int) -> array.array:
    with wave.open(str(caminho), "rb") as w:
        if (w.getnchannels(), w.getsampwidth(), w.getframerate()) != (1, 2, taxa):
            raise SystemExit(f"{caminho} não é mono, 16 bits, {taxa} Hz")
        amostras = array.array("h", w.readframes(w.getnframes()))
    if sys.byteorder == "big":
        amostras.byteswap()
    return amostras


def logo_sonoro(taxa: int, duracao_s: float) -> array.array:
    expr = LOGO.format(d=duracao_s).replace(",", "\\,")
    feito = subprocess.run([_ffmpeg(), "-v", "error", "-f", "lavfi", "-i",
                            f"aevalsrc=exprs={expr}:s={taxa}:d={duracao_s}",
                            "-f", "s16le", "-ac", "1", "-ar", str(taxa), "-"], capture_output=True)
    if feito.returncode != 0:
        raise SystemExit(f"o aevalsrc falhou: {feito.stderr.decode(errors='replace')[-1000:]}")
    amostras = array.array("h", feito.stdout)
    if sys.byteorder == "big":
        amostras.byteswap()
    return amostras


def misturar(linha: dict, pico_dbfs: float, falas: dict[str, array.array], logo: array.array) -> array.array:
    """Põe cada fala na amostra dela e o logo no marca_em, e leva o pico da soma a `pico_dbfs`."""
    taxa, fps = linha["taxa_do_som"], linha["fps"]
    total = linha["quadros"] * (taxa // fps)
    faixa = [0] * total
    for seg in linha["segmentos"]:
        amostras = falas[seg["chave"]]
        inicio = seg["voz_inicio_amostra"]
        if inicio + len(amostras) > total:
            raise ValueError(f"a fala {seg['chave']} passa do fim do anúncio")
        for i, a in enumerate(amostras):
            faixa[inicio + i] += a
    pico_da_fala = max(max(abs(a) for a in amostras) for amostras in falas.values())
    pico_do_logo = max(abs(a) for a in logo) or 1
    inicio = linha["marca_em"] * (taxa // fps)
    for i, a in enumerate(logo):
        if inicio + i < total:
            faixa[inicio + i] += round(a * pico_da_fala / pico_do_logo)
    pico = max(abs(a) for a in faixa) or 1
    alvo = 32767 * 10 ** (pico_dbfs / 20)
    return array.array("h", (max(-32768, min(32767, round(a * alvo / pico))) for a in faixa))


def main(anuncio: str) -> int:
    params = json.loads(parametros(anuncio).read_text(encoding="utf-8"))
    linha = json.loads((LINHA / f"{anuncio}.json").read_text(encoding="utf-8"))
    brutos = json.loads(BRUTOS_JSON.read_text(encoding="utf-8"))
    taxa = linha["taxa_do_som"]
    falas = {}
    for seg in linha["segmentos"]:
        caminho = BRUTOS / f"{seg['chave']}.wav"
        if hashlib.sha256(caminho.read_bytes()).hexdigest() != brutos["falas"][seg["chave"]]["sha256"]:
            raise SystemExit(f"o bruto {caminho} não é o do brutos.json")
        falas[seg["chave"]] = _ler_wav(caminho, taxa)
    faixa = misturar(linha, params["pico_dbfs"], falas, logo_sonoro(taxa, linha["logo_sonoro_s"]))
    if sys.byteorder == "big":
        faixa.byteswap()
    pasta = MONTAGEM / anuncio
    pasta.mkdir(parents=True, exist_ok=True)
    saida = pasta / "som.wav"
    with wave.open(str(saida), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(taxa)
        w.writeframes(faixa.tobytes())
    print(f"{saida}: {len(faixa) / taxa:.3f} s, sha256 {hashlib.sha256(saida.read_bytes()).hexdigest()[:12]}")
    return 0
