"""Onde mora cada coisa. O que é mídia fica fora do git, em $VIDEOS."""

from __future__ import annotations

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACOTE = RAIZ / "anuncios"
FONTES = PACOTE / "fontes"
FALA = PACOTE / "fala"
LINHA = PACOTE / "linha_do_tempo"
BRUTOS_JSON = PACOTE / "brutos.json"

# A pasta dos vídeos, fora do git (bloco 3 do docs/ROADMAP.md). Sem a variável, é a pasta irmã do repositório.
VIDEOS = Path(os.environ.get("VIDEOS") or RAIZ.parent / "vesk-hack-videos")
BRUTOS = VIDEOS / "brutos"
MONTAGEM = VIDEOS / "montagem"
PROVAS = VIDEOS / "provas"
PROIBIDO = VIDEOS / "proibido.txt"


def parametros(anuncio: str) -> Path:
    if anuncio not in ("a", "b"):
        raise ValueError(f"o anúncio é a ou b, não {anuncio!r}")
    return PACOTE / f"{anuncio}.json"
