"""O áudio de um anúncio ($VIDEOS/montagem/<a|b>/som.wav): cada fala no quadro dela, o logo sonoro na cartela e os
efeitos discretos (um sopro antes de cada corte e um clique nas duas ações da tela). É o mesmo nas duas histórias.

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

from anuncios.caminhos import BRUTOS, BRUTOS_JSON, LINHA, MONTAGEM, PACOTE, parametros

# Escolha de desenho: duas notas senoidais, lá5 (880 Hz) e mi6 (1318,51 Hz, a quinta acima), a segunda entrando em
# 0,12 s; cada uma com 4 ms de ataque e queda exponencial, e 20 ms de saída no fim para não estalar.
LOGO = ("(sin(2*PI*880*t)*min(t/0.004,1)*exp(-12*t)"
        "+gte(t,0.12)*sin(2*PI*1318.51*(t-0.12))*min((t-0.12)/0.004,1)*exp(-6*(t-0.12)))"
        "*min(({d}-t)/0.02,1)")


# Os efeitos (16/11/2026) são os da biblioteca que vem com o HyperFrames 0.9.33 (anuncios/hyperframes, `npm ci`), do
# Pixabay, sob a Pixabay Content License (https://pixabay.com/service/license-summary/): uso comercial e remix sem
# atribuição, e a redistribuição só dentro de uma obra derivada, como o vídeo. Por isso o mp3 não entra no git: ele é
# lido do node_modules e conferido pelo sha256.
SFX = PACOTE / "hyperframes/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx"
EFEITOS = {
    "whoosh-short": "c2efd9d902a59bf9ec5019035d7deadd17762136896b6e3cb6dd99ea50997a30",
    "click-soft": "075e17bdac5c13662a1c9530050e0046f81d4138e00eb3bf30427a7b4404103d",
}
# Escolha de desenho: o sopro começa 0,12 s antes de cada corte, menos o da cartela, onde toca o logo sonoro; o clique
# cai na palavra da ação da tela. Os dois ficam bem abaixo do pico da fala.
SOPRO_ANTES_S = 0.12
GANHO_DB = {"whoosh-short": -18.0, "click-soft": -14.0}
CLIQUES = (("variante", "one"), ("chamada", "Upload"))


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


def onde_os_efeitos(linha: dict) -> list[tuple[str, int]]:
    """Cada efeito e a amostra em que ele começa: o sopro antes dos cortes (menos o da cartela) e os cliques."""
    taxa, fps = linha["taxa_do_som"], linha["fps"]
    por_quadro = taxa // fps
    lista = [("whoosh-short", c * por_quadro - round(SOPRO_ANTES_S * taxa))
             for c in linha["cortes"] if c != linha["marca_em"]]
    for chave, texto in CLIQUES:
        seg = next(s for s in linha["segmentos"] if s["chave"] == chave)
        p = next(p for p in seg["palavras"] if p["texto"].strip(".,?!;:") == texto)
        lista.append(("click-soft", p["inicio"] * por_quadro))
    return sorted(lista, key=lambda e: e[1])


def efeito(nome: str, taxa: int) -> array.array:
    caminho = SFX / f"{nome}.mp3"
    if not caminho.is_file():
        raise SystemExit(f"falta o {caminho}: rode `npm ci` em anuncios/hyperframes")
    if hashlib.sha256(caminho.read_bytes()).hexdigest() != EFEITOS[nome]:
        raise SystemExit(f"o {caminho} não é o do HyperFrames 0.9.33 (o sha256 mudou)")
    feito = subprocess.run([_ffmpeg(), "-v", "error", "-i", str(caminho), "-f", "s16le", "-ac", "1", "-ar", str(taxa),
                            "-"], capture_output=True)
    if feito.returncode != 0:
        raise SystemExit(f"o ffmpeg não leu o {caminho}: {feito.stderr.decode(errors='replace')[-1000:]}")
    amostras = array.array("h", feito.stdout)
    if sys.byteorder == "big":
        amostras.byteswap()
    return amostras


def misturar(linha: dict, pico_dbfs: float, falas: dict[str, array.array], logo: array.array,
             efeitos: list[tuple[array.array, int, float]] = ()) -> array.array:
    """Põe cada fala na amostra dela, o logo no marca_em e cada efeito (amostras, início, ganho em dB sobre o pico da
    fala) no lugar dele, e leva o pico da soma a `pico_dbfs`."""
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
    for amostras, inicio, ganho_db in efeitos:
        escala = pico_da_fala * 10 ** (ganho_db / 20) / (max(abs(a) for a in amostras) or 1)
        for i, a in enumerate(amostras):
            if 0 <= inicio + i < total:
                faixa[inicio + i] += round(a * escala)
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
    sons = {nome: efeito(nome, taxa) for nome in EFEITOS}
    efeitos = [(sons[nome], inicio, GANHO_DB[nome]) for nome, inicio in onde_os_efeitos(linha)]
    faixa = misturar(linha, params["pico_dbfs"], falas, logo_sonoro(taxa, linha["logo_sonoro_s"]), efeitos)
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
