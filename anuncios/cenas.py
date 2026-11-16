"""A raiz do projeto do HyperFrames (anuncios/hyperframes/index.html), escrita a partir da linha do tempo de um anúncio.

    python -m anuncios cenas a|b [--historia 2|3]

A raiz monta uma cena por fala, cada uma no quadro da linha do tempo, e passa às cenas, em window.VESK, o tempo de
cada palavra contado do começo da cena. A e B usam as mesmas cenas; só a raiz muda. A marca e a chamada são iguais nas
duas histórias. As fontes de anuncios/fontes vão para assets/fontes, e o GSAP fixado no package.json vai para
assets/gsap.min.js, os dois fora do git: o HyperFrames só lê o que está dentro do projeto, e o render não usa rede.

Cada cena começa 1/4 de quadro antes do quadro dela: o quadro n cai em n/30 s, e com a cena em exatamente n/30 a
igualdade de ponto flutuante decide se o primeiro quadro é da cena nova ou da anterior. Com o quarto de quadro, o
quadro n já é da cena nova e o n-1 ainda é da anterior, de qualquer jeito que o tempo seja arredondado.
"""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from anuncios.caminhos import FONTES, LINHA, PACOTE
from anuncios.falas import CHAVE_DA_MARCA

PROJETO = PACOTE / "hyperframes"
COMUNS = (CHAVE_DA_MARCA, "chamada")  # as cenas que as duas histórias dividem
HISTORIAS = ("2", "3")
ANTECIPA = 0.25  # em quadros


def _s(quadros: float, fps: int) -> str:
    return f"{quadros / fps:.6f}"


def composicao(chave: str, historia: str) -> str:
    return chave if chave in COMUNS else f"h{historia}-{chave}"


def raiz(linha: dict, anuncio: str, historia: str) -> str:
    fps = linha["fps"]
    hosts = []
    dados = {}
    for i, seg in enumerate(linha["segmentos"]):
        cid = composicao(seg["chave"], historia)
        inicio = max(seg["inicio"] - ANTECIPA, 0)
        fim = seg["fim"] - ANTECIPA if seg["fim"] < linha["quadros"] else seg["fim"]
        hosts.append(
            f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"\n'
            f'        data-start="{_s(inicio, fps)}" data-duration="{_s(fim - inicio, fps)}" data-track-index="{i + 1}"\n'
            f'        data-track-kind="graphics" data-width="{linha["largura"]}" data-height="{linha["altura"]}"></div>'
        )
        dados[seg["chave"]] = {
            "chave": seg["chave"],
            "quadros": seg["fim"] - seg["inicio"],
            "palavras": [{"texto": p["texto"], "inicio": p["inicio"] - seg["inicio"], "fim": p["fim"] - seg["inicio"]}
                         for p in seg["palavras"]],
        }
    vesk = {"anuncio": anuncio, "historia": historia, "fps": fps, "marca_em": linha["marca_em"],
            "cartela_marca": linha["cartela_marca"], "segmentos": dados}
    cid_raiz = f"anuncio-{anuncio}"
    return f"""<!doctype html>
<!-- Gerado por `python -m anuncios cenas {anuncio} --historia {historia}` a partir de anuncios/linha_do_tempo/{anuncio}.json.
     Não edite à mão: o tempo vem da linha do tempo. -->
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{html.escape(f"Vesk, anúncio {anuncio.upper()}")}</title>
    <link rel="stylesheet" href="assets/vesk.css" />
    <script src="assets/gsap.min.js"></script>
    <script src="assets/kit.js"></script>
    <script>
      window.VESK = {json.dumps(vesk, ensure_ascii=False)};
    </script>
    <style>
      html, body {{ margin: 0; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{cid_raiz}" data-start="0" data-duration="{_s(linha["quadros"], fps)}"
      data-width="{linha["largura"]}" data-height="{linha["altura"]}">
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines["{cid_raiz}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def _copiar(origem: Path, alvo: Path) -> None:
    if not alvo.is_file() or alvo.read_bytes() != origem.read_bytes():
        shutil.copyfile(origem, alvo)


def copiar_dependencias() -> None:
    destino = PROJETO / "assets" / "fontes"
    destino.mkdir(parents=True, exist_ok=True)
    for ttf in FONTES.glob("*/*.ttf"):
        _copiar(ttf, destino / ttf.name)
    gsap = PROJETO / "node_modules" / "gsap" / "dist" / "gsap.min.js"
    if not gsap.is_file():
        raise SystemExit(f"falta o {gsap}: rode `npm ci` em {PROJETO}")
    _copiar(gsap, PROJETO / "assets" / "gsap.min.js")


def main(anuncio: str, historia: str = "2") -> int:
    if historia not in HISTORIAS:
        print(f"erro: a história é uma de {HISTORIAS}, não {historia!r}")
        return 2
    linha = json.loads((LINHA / f"{anuncio}.json").read_text(encoding="utf-8"))
    faltam = [composicao(s["chave"], historia) for s in linha["segmentos"]
              if not (PROJETO / "compositions" / f"{composicao(s['chave'], historia)}.html").is_file()]
    if faltam:
        print(f"erro: faltam as cenas {faltam} em {PROJETO / 'compositions'}")
        return 2
    copiar_dependencias()
    saida = PROJETO / "index.html"
    saida.write_text(raiz(linha, anuncio, historia), encoding="utf-8")
    print(f"{saida}: anúncio {anuncio}, história {historia}, {linha['quadros']} quadros, marca_em {linha['marca_em']}")
    return 0
