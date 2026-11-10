"""Gera a suíte de sintéticos da C7: 24 vídeos, cada um com o gabarito.json ao lado.

    python -m exemplos.suite --saida <pasta>

A lista é fixa (escrita aqui, não sorteada). Ela varia o segundo da marca, a duração,
a fala e os cortes (pela semente). Dois vídeos não têm a marca: são o controle negativo.
O piso de 20 vídeos tem conta: com 20 acertos em 20, o limite de baixo do intervalo de
Wilson de 95% fica em cerca de 84% (20 / (20 + 1,96²)).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from exemplos.sintetico import FaltaFerramenta, gerar

# (marca_em, duração, semente, fala, marca)
SUITE = (
    (1, 10, 101, True, True),
    (2, 10, 102, True, True),
    (3, 10, 103, True, True),
    (5, 10, 104, False, True),
    (8, 10, 105, True, True),
    (1, 15, 106, True, True),
    (2, 15, 107, True, True),
    (3, 15, 108, False, True),
    (4, 15, 109, True, True),
    (5, 15, 110, True, True),
    (6, 15, 111, True, True),
    (7, 15, 112, True, True),
    (9, 15, 113, True, True),
    (2, 20, 114, True, True),
    (4, 20, 115, True, True),
    (6, 20, 116, False, True),
    (8, 20, 117, True, True),
    (9, 20, 118, True, True),
    (1, 30, 119, True, True),
    (3, 30, 120, True, True),
    (5, 30, 121, True, True),
    (7, 30, 122, False, True),
    (4, 15, 123, True, False),
    (6, 30, 124, True, False),
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m exemplos.suite", description=__doc__.split("\n")[0])
    p.add_argument("--saida", type=Path, required=True, help="pasta da suíte (uma subpasta sNN por vídeo)")
    a = p.parse_args(argv)
    indice = []
    try:
        for n, (marca_em, duracao, semente, fala, marca) in enumerate(SUITE, start=1):
            nome = f"s{n:02d}"
            video = a.saida / nome / "video.mp4"
            g = gerar(marca_em, semente, video, duracao, fala=fala, marca=marca)
            indice.append({"nome": nome, "video": f"{nome}/video.mp4", "gabarito": f"{nome}/gabarito.json",
                           "marca_em": g["marca_em"], "duracao": g["duracao"], "semente": semente,
                           "fala": fala, "marca": marca})
            print(f"{nome}: marca_em={g['marca_em']} duracao={g['duracao']} cortes={len(g['cortes'])}")
    except (FaltaFerramenta, ValueError) as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    (a.saida / "suite.json").write_text(json.dumps({"videos": indice}, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")
    print(f"{len(indice)} vídeos em {a.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
