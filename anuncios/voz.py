"""As seis falas na voz do Kokoro-82M `af_heart`, em $VIDEOS/brutos/<chave>.wav, com o sha256 em anuncios/brutos.json.

Roda no Python 3.11, pelo uv, porque no 3.14 o kokoro 0.9.4 não instala (anuncios/requisitos-voz.in):

    uv run --no-project --python 3.11 --with-requirements anuncios/requisitos-voz.txt python -X utf8 -m anuncios voz
    (o mesmo comando, com --conferir no fim, gera de novo numa pasta temporária e compara o sha256)

O decodificador do Kokoro soma ruído aleatório, e por isso a semente é fixada antes de cada fala.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import wave
from pathlib import Path

from anuncios.caminhos import BRUTOS, BRUTOS_JSON
from anuncios.falas import CHAVES, FALAS, conferir_proibido

REPO = "hexgrad/Kokoro-82M"
VOZ = "af_heart"  # nota «A» no VOICES.md do Kokoro-82M (skill video)
TAXA = 24000  # a taxa de saída do Kokoro-82M
SEMENTE = 20261111  # um inteiro fixo qualquer: a data do plano aprovado
FIOS = 2  # threads do torch: as mesmas cpus que o job da fila declara, para a soma em ponto flutuante não mudar


def _sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def _gravar_wav(caminho: Path, pcm: bytes) -> None:
    with wave.open(str(caminho), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TAXA)
        w.writeframes(pcm)


def gerar(destino: Path) -> dict:
    import numpy as np
    import torch
    from huggingface_hub import hf_hub_download
    from kokoro import KPipeline

    import kokoro

    conferir_proibido()
    torch.set_num_threads(FIOS)
    pipeline = KPipeline(lang_code="a", repo_id=REPO)
    destino.mkdir(parents=True, exist_ok=True)

    falas = {}
    for chave in CHAVES:
        torch.manual_seed(SEMENTE)
        partes = [r.audio for r in pipeline(FALAS[chave]["voz"], voice=VOZ, speed=1) if r.audio is not None]
        if not partes:
            raise SystemExit(f"o Kokoro não devolveu áudio para a fala {chave}")
        audio = torch.cat(partes).detach().cpu().numpy().astype(np.float64)
        pcm = np.clip(np.rint(audio * 32767.0), -32768, 32767).astype("<i2").tobytes()
        caminho = destino / f"{chave}.wav"
        _gravar_wav(caminho, pcm)
        amostras = len(pcm) // 2
        falas[chave] = {"arquivo": f"brutos/{chave}.wav", "sha256": _sha256(caminho), "amostras": amostras,
                        "duracao": round(amostras / TAXA, 6)}
        print(f"{chave}: {amostras / TAXA:.3f} s, sha256 {falas[chave]['sha256'][:12]}")

    # A procedência do modelo: a revisão do Hugging Face que o cache usou e o sha256 dos pesos e da voz.
    pesos = Path(hf_hub_download(REPO, "kokoro-v1_0.pth"))
    voz = Path(hf_hub_download(REPO, f"voices/{VOZ}.pt"))
    return {
        "voz": {
            "modelo": REPO,
            "revisao": pesos.parent.name,
            "pesos_sha256": _sha256(pesos),
            "voz": VOZ,
            "voz_sha256": _sha256(voz),
            "kokoro": getattr(kokoro, "__version__", "0.9.4"),
            "torch": torch.__version__,
            "python": sys.version.split()[0],
            "semente": SEMENTE,
            "fios": FIOS,
            "taxa": TAXA,
        },
        "falas": falas,
    }


def main(conferir: bool = False) -> int:
    if not conferir:
        registro = gerar(BRUTOS)
        BRUTOS_JSON.write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"gravado {BRUTOS_JSON}")
        return 0

    anotado = json.loads(BRUTOS_JSON.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="voz-") as tmp:
        de_novo = gerar(Path(tmp))
    diferentes = [c for c in CHAVES if de_novo["falas"][c]["sha256"] != anotado["falas"][c]["sha256"]]
    for c in CHAVES:
        igual = "igual" if c not in diferentes else "DIFERENTE"
        print(f"{c}: {igual} ({de_novo['falas'][c]['sha256'][:12]} contra {anotado['falas'][c]['sha256'][:12]})")
    return 1 if diferentes else 0
