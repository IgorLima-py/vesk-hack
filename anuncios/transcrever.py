"""O tempo de cada palavra dos brutos, pelo faster-whisper, com a grafia do roteiro.

O whisper dá o tempo, e o roteiro dá a grafia: a marca nunca sai escrita como o whisper ouviu. Se o whisper ouvir
mais ou menos palavras do que o roteiro tem, o comando para e diz quais. O resultado vai para anuncios/fala/<chave>.json,
no git, e é dele que a linha do tempo sai.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import wave
from pathlib import Path

from anuncios.caminhos import BRUTOS, BRUTOS_JSON, FALA
from anuncios.falas import CHAVES, FALAS

MODELO = "small"  # o faster-whisper-small, que já está no cache do Hugging Face na Karen
FIOS = 2  # as cpus que o job da fila declara


def _normal(palavra: str) -> str:
    return re.sub(r"[^a-z0-9']", "", palavra.lower())


def alinhar(texto: str, ouvidas: list[tuple[str, float, float]]) -> list[dict]:
    """Junta a grafia do roteiro ao tempo do whisper, palavra a palavra, na ordem.

    `ouvidas` é a lista (palavra, início, fim) do whisper. Com o mesmo número de palavras, a grafia é a do roteiro.
    Com número diferente, levanta ValueError dizendo o que faltou e o que sobrou.
    """
    escritas = texto.split()
    if len(escritas) != len(ouvidas):
        a = [_normal(p) for p in escritas]
        b = [_normal(p) for p, _, _ in ouvidas]
        faltam: list[str] = []
        sobram: list[str] = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
            if tag == "replace" and i2 - i1 == j2 - j1:
                continue  # a mesma quantidade escrita de outro jeito («Vesque» por «Vesk»): o roteiro já resolve
            if tag in ("delete", "replace"):
                faltam += escritas[i1:i2]
            if tag in ("insert", "replace"):
                sobram += [ouvidas[j][0].strip() for j in range(j1, j2)]
        raise ValueError(f"o whisper ouviu {len(ouvidas)} palavras e o roteiro tem {len(escritas)}: "
                         f"faltam {faltam}, sobram {sobram}")
    return [{"texto": escrita, "inicio": round(float(inicio), 3), "fim": round(float(fim), 3)}
            for escrita, (_, inicio, fim) in zip(escritas, ouvidas)]


def main() -> int:
    from faster_whisper import WhisperModel

    import faster_whisper

    brutos = json.loads(BRUTOS_JSON.read_text(encoding="utf-8"))
    modelo = WhisperModel(MODELO, device="cpu", compute_type="int8", cpu_threads=FIOS, local_files_only=True)
    FALA.mkdir(parents=True, exist_ok=True)
    erros = []
    for chave in CHAVES:
        wav = BRUTOS / f"{chave}.wav"
        sha = hashlib.sha256(wav.read_bytes()).hexdigest()
        if sha != brutos["falas"][chave]["sha256"]:
            raise SystemExit(f"o bruto {wav} não é o do brutos.json; rode a voz de novo")
        with wave.open(str(wav), "rb") as w:
            duracao = w.getnframes() / w.getframerate()
        segmentos, _ = modelo.transcribe(str(wav), language="en", word_timestamps=True, beam_size=5,
                                         temperature=0.0, condition_on_previous_text=False, vad_filter=False)
        ouvidas = [(p.word, p.start, p.end) for s in segmentos for p in (s.words or [])]
        ouvido = " ".join(p.strip() for p, _, _ in ouvidas)
        try:
            palavras = alinhar(FALAS[chave]["texto"], ouvidas)
        except ValueError as erro:
            erros.append(f"{chave}: {erro} (ouvido: {ouvido!r})")
            continue
        saida = {
            "chave": chave,
            "texto": FALAS[chave]["texto"],
            "ouvido": ouvido,
            "bruto_sha256": sha,
            "duracao": round(duracao, 6),
            "palavras": palavras,
            "whisper": {"faster_whisper": faster_whisper.__version__, "modelo": MODELO, "compute_type": "int8"},
        }
        (FALA / f"{chave}.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        primeira, ultima = palavras[0], palavras[-1]
        print(f"{chave}: {duracao:.3f} s; fala de {primeira['inicio']:.3f} a {ultima['fim']:.3f} s; ouvido: {ouvido}")
    for erro in erros:
        print(f"erro: {erro}")
    return 1 if erros else 0
