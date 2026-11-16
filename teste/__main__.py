"""O plano do teste A/B.

    python -m teste poder --p1 <taxa> --p2 <taxa> [--alfa 0.05] [--poder 0.8]

Imprime o n por braço de um teste bicaudal de duas proporções, com a fórmula e a fonte (teste/poder.py). Com p1
igual a p2 não há efeito a detectar, e sai 2.
"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m teste", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="comando", required=True)
    pw = sub.add_parser("poder", help="o n por braço de um teste A/B de duas proporções")
    pw.add_argument("--p1", type=float, required=True, help="a taxa esperada no braço A (ex.: 0.30)")
    pw.add_argument("--p2", type=float, required=True, help="a taxa que se quer detectar no braço B (ex.: 0.33)")
    pw.add_argument("--alfa", type=float, default=0.05, help="o nível de significância, bicaudal (padrão 0.05)")
    pw.add_argument("--poder", type=float, default=0.8, help="a chance de detectar o efeito, se ele existe (padrão 0.8)")
    a = p.parse_args(argv)

    from teste.poder import calcular, texto

    try:
        plano = calcular(a.p1, a.p2, a.alfa, a.poder)
    except ValueError as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    print(texto(plano))
    return 0


if __name__ == "__main__":
    sys.exit(main())
