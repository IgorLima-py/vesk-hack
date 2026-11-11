"""python -m anuncios <comando>

    voz [--conferir]      as seis falas no Kokoro (Python 3.11, pelo uv; o comando inteiro em anuncios/voz.py)
    transcrever           o tempo de cada palavra (faster-whisper), com a grafia do roteiro
    tempo a|b             a linha do tempo, a única entrada dos motores
    som a|b               o áudio: as falas no quadro delas e o logo sonoro na cartela da marca
    final a|b --imagem X  queima a legenda na imagem muda do motor, junta o som, grava o mp4 e o gabarito
    prova <motor> ...     as medidas de uma frente da prova dos motores

Cada comando importa só o que usa: os testes e o Python 3.14 não precisam do kokoro.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m anuncios", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="comando", required=True)

    voz = sub.add_parser("voz", help="as seis falas no Kokoro")
    voz.add_argument("--conferir", action="store_true", help="gera de novo e compara o sha256 com o brutos.json")

    sub.add_parser("transcrever", help="o tempo de cada palavra, com a grafia do roteiro")

    for nome in ("tempo", "som"):
        s = sub.add_parser(nome)
        s.add_argument("anuncio", choices=("a", "b"))

    final = sub.add_parser("final", help="legenda, som, mp4 e gabarito")
    final.add_argument("anuncio", choices=("a", "b"))
    final.add_argument("--imagem", type=Path, required=True, help="o mp4 mudo que o motor renderizou")
    final.add_argument("--saida", type=Path, help="o mp4 final (padrão: $VIDEOS/<a|b>.mp4)")

    prova = sub.add_parser("prova", help="as medidas de uma frente da prova")
    prova.add_argument("motor")
    prova.add_argument("--render", type=Path, action="append", required=True,
                       help="um mp4 mudo do A; passe dois, de dois renders")
    prova.add_argument("--projeto", type=Path, required=True, help="a pasta do projeto do motor")
    prova.add_argument("--pacote", help="o pacote npm do motor, para ler a licença em node_modules")

    a = p.parse_args(argv)
    if a.comando == "voz":
        from anuncios import voz as m
        return m.main(conferir=a.conferir)
    if a.comando == "transcrever":
        from anuncios import transcrever as m
        return m.main()
    if a.comando == "tempo":
        from anuncios import tempo as m
        return m.main(a.anuncio)
    if a.comando == "som":
        from anuncios import som as m
        return m.main(a.anuncio)
    if a.comando == "final":
        from anuncios import final as m
        return m.main(a.anuncio, a.imagem, a.saida)
    if a.comando == "prova":
        from anuncios import prova as m
        return m.main(a.motor, a.render, a.projeto, a.pacote)
    return 2


if __name__ == "__main__":
    sys.exit(main())
