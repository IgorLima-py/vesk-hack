"""A variante de uma mudança só e a conferência dela.

    python -m variante gerar --video <mp4> --marca-em <s> --mudanca marca_no_inicio --saida <pasta>
    python -m variante conferir <pasta>

`gerar` grava na pasta o `variante.mp4` e o `certificado.json`. `conferir` decodifica de novo o original e a variante
e sai 0 só se fora do trecho tudo é igual, se o trecho mudou de fato para o quadro da marca e se o áudio não mexeu.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from variante.quadros import FaltaFerramenta, VideoInvalido


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m variante", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="comando", required=True)

    g = sub.add_parser("gerar", help="grava a variante e o certificado")
    g.add_argument("--video", type=Path, required=True, help="o mp4 original")
    g.add_argument("--marca-em", type=float, required=True, help="o segundo em que a marca aparece no original")
    g.add_argument("--mudanca", required=True, choices=["marca_no_inicio"],
                   help="marca_no_inicio: o 1º segundo vira o quadro da marca")
    g.add_argument("--saida", type=Path, required=True, help="a pasta do variante.mp4 e do certificado.json")

    c = sub.add_parser("conferir", help="confere a variante contra o original, quadro a quadro")
    c.add_argument("pasta", type=Path, help="a pasta com o certificado.json e a variante")

    a = p.parse_args(argv)
    if a.comando == "gerar":
        from variante.gerar import gerar

        try:
            cert = gerar(a.video, a.marca_em, a.mudanca, a.saida)
        except (FaltaFerramenta, VideoInvalido, ValueError) as erro:
            print(f"erro: {erro}", file=sys.stderr)
            return 2
        t = cert["trecho"]
        print(f"{a.saida / cert['variante']['arquivo']} (sha256 {cert['variante']['sha256']})")
        print(f"trecho mudado: [{t['inicio']}, {t['fim']}) s, quadros {t['quadro_inicio']} a {t['quadro_fim'] - 1}, "
              f"todos iguais ao quadro {cert['quadro_da_marca']['n']} do original "
              f"({cert['quadro_da_marca']['pts']} s); {len(cert['fora'])} quadros fora do trecho, sem perda")
        return 0

    from variante.conferir import CertificadoInvalido, conferir

    try:
        checagens = conferir(a.pasta)
    except (FaltaFerramenta, VideoInvalido, CertificadoInvalido) as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    for ch in checagens:
        print(f"{'ok    ' if ch.ok else 'FALHA '} {ch.texto}")
    falhas = sum(not ch.ok for ch in checagens)
    print("a variante muda uma coisa só, e só no trecho declarado" if not falhas
          else f"{falhas} checagem(ns) falharam")
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
