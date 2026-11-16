"""O roteiro dos anúncios A e B: seis falas em inglês, para o público dos EUA (plano aprovado pelo Igor em 11/11/2026).

Cada fala tem:
- `texto`: a grafia, que vai para a legenda e para o gabarito;
- `voz`: o que o Kokoro lê. É o mesmo texto, com a pronúncia fixada onde o inglês é ambíguo ou a palavra é nossa;
- `tela`: por linha de história (anuncios/storylines.md), todo texto que o motor escreve na tela, sem número nenhum. Cada
  item vale desde o primeiro quadro da fala, ou desde a palavra `desde_palavra`, até o fim dela ou até a palavra
  `ate_palavra`. Repetido na tela (os dois cartões da variante), conta uma vez;
- `desenho`: por linha de história, o que o motor desenha no segmento.

As duas histórias (16/11/2026) usam a mesma voz, os mesmos cortes e o mesmo `marca_em`; a marca e a chamada são as
mesmas cenas nas duas.
"""

from __future__ import annotations

import re

from anuncios.caminhos import PROIBIDO

CHAVES = ("gancho", "problema", "leitura", "variante", "marca", "chamada")
CHAVE_DA_MARCA = "marca"

HISTORIAS = ("2", "3")

# O cartão do anúncio no feed (VeskKit.Anuncio), genérico, sem a marca de plataforma nenhuma.
_CARTAO = [{"texto": "yourbrand", "papel": "cartao"}, {"texto": "Sponsored", "papel": "cartao"},
           {"texto": "Shop now", "papel": "cartao"}]


def _nas_duas(valor):
    return {h: valor for h in HISTORIAS}


FALAS: dict[str, dict] = {
    "gancho": {
        "texto": "Your ad is losing people in the first seconds.",
        "voz": "Your ad is losing people in the first seconds.",
        "tela": {
            "2": [{"texto": "Your ad is losing people in the first seconds.", "papel": "frase_em_cinza"},
                  *_CARTAO, {"texto": "Viewers", "papel": "rotulo"}],
            "3": [{"texto": "Your ad is losing people in the first seconds.", "papel": "frase_em_cinza"}],
        },
        "desenho": {
            "2": "O anúncio no feed, rodando a abertura, e à direita quem o assiste, um ponto por pessoa; no penhasco "
                 "dos primeiros segundos, os pontos se apagam. A frase está em cinza desde o quadro 0, e cada palavra "
                 "vira tinta quando é dita; «first seconds.» ganha o grifo.",
            "3": "«losing people» enorme sobre uma mancha de pontos que se apaga ponto a ponto. A frase está em cinza "
                 "desde o quadro 0, e cada palavra vira tinta quando é dita; «first seconds.» ganha o grifo.",
        },
    },
    "problema": {
        "texto": "You can see when they leave. Not why.",
        "voz": "You can see when they leave. Not why.",
        "tela": {
            "2": [{"texto": "Drop-off", "papel": "rotulo", "desde_palavra": "when"},
                  {"texto": "?", "papel": "interrogacao", "desde_palavra": "Not"}],
            "3": [{"texto": "You can see when they leave.", "papel": "frase_em_cinza", "ate_palavra": "Not"},
                  {"texto": "Not", "papel": "frase", "desde_palavra": "Not"},
                  {"texto": "why.", "papel": "frase", "desde_palavra": "why"}],
        },
        "desenho": {
            "2": "De perto, no penhasco: o anel e «Drop-off» em «when»; o «?» enorme no vazio de quem saiu, em «Not».",
            "3": "A frase chega palavra a palavra; em «Not», sai num borrão, e «Not why.» ocupa a largura, com «why.» "
                 "grifado.",
        },
    },
    "leitura": {
        "texto": "We read your video, second by second, and match it to the moment people drop off.",
        "voz": "We [read](/ɹˈid/) your video, second by second, and match it to the moment people drop off.",
        "tela": {
            "2": [{"texto": "Readout", "papel": "rotulo"}, {"texto": "Logo", "papel": "rotulo"},
                  {"texto": "Product", "papel": "rotulo"}, {"texto": "Cut", "papel": "rotulo"},
                  {"texto": "Logo only, no product", "papel": "leitura", "desde_palavra": "video"},
                  {"texto": "Product enters late", "papel": "leitura", "desde_palavra": "second"},
                  {"texto": "Close-up, no text", "papel": "leitura", "desde_palavra": "and"}],
            "3": [{"texto": "second", "papel": "rolo"},
                  {"texto": "Drop-off", "papel": "rotulo", "desde_palavra": "drop"}],
        },
        "desenho": {
            "2": "A tela do produto: o anúncio lido em mosaico, as linhas da leitura com o selo, a curva e as faixas "
                 "do que estava na tela. O cabeçote corre o anúncio, volta ao penhasco em «match», e a linha que "
                 "explica a saída é grifada em «drop».",
            "3": "Um rolo de «second» corre pelo cabeçote; freia em «match», e em «drop» o segundo parado no cabeçote "
                 "é grifado e ganha «Drop-off».",
        },
    },
    "variante": {
        "texto": "Then you get a variant with one change, ready to test.",
        "voz": "Then you get a variant with one change, ready to test.",
        "tela": {
            "2": [{"texto": "Control", "papel": "rotulo"},
                  {"texto": "Variant", "papel": "rotulo", "desde_palavra": "variant"},
                  *_CARTAO, {"texto": "One change", "papel": "etiqueta", "desde_palavra": "one"}],
            "3": [{"texto": "Control", "papel": "rotulo"}, {"texto": "Variant", "papel": "rotulo"},
                  {"texto": "Logo first.", "papel": "frase"},
                  {"texto": "Bottle first.", "papel": "frase", "desde_palavra": "one"}],
        },
        "desenho": {
            "2": "Control e variant, os dois no cartão do feed, iguais; em «one», só a variante muda: o frasco entra "
                 "na abertura, contornado no grifo, com a etiqueta «One change».",
            "3": "Control e variant, «Logo first.» nas duas; em «one», a linha da variante roda e para em «Bottle "
                 "first.», com «Bottle» grifado, e a do controle ganha um risco.",
        },
    },
    "marca": {
        "texto": "Vesk. The creative autopilot.",
        "voz": "[Vesk](/vˈɛsk/). The creative autopilot.",
        "tela": _nas_duas([
            {"texto": "Vesk", "papel": "wordmark"},
            {"texto": "The creative autopilot for video ads.", "papel": "assinatura"},
        ]),
        "desenho": _nas_duas(
            "A cartela da marca: fundo preto; o selo de três pontos do site, grande, com o degradê da paleta do "
            "campo; o wordmark «Vesk» em Newsreader peso 500, centrado, logo acima da barra; a barra do grifo ocupa "
            "exatamente o retângulo cartela_marca.barra; e «The creative autopilot for video ads.» em Schibsted "
            "Grotesk logo abaixo dela. Tudo entra inteiro no primeiro quadro do segmento, que é o marca_em, sem "
            "animação de entrada. Nada no grifo pode ocupar o retângulo da barra antes desse quadro."
        ),
    },
    "chamada": {
        "texto": "Upload your ad. Get the report.",
        "voz": "Upload your ad. Get the report.",
        "tela": _nas_duas([
            {"texto": "vesklab.com", "papel": "endereco"}, *_CARTAO, {"texto": "Readout", "papel": "rotulo"},
            {"texto": "Logo only, no product", "papel": "leitura", "desde_palavra": "report"},
            {"texto": "Product enters late", "papel": "leitura", "desde_palavra": "report"},
            {"texto": "Close-up, no text", "papel": "leitura", "desde_palavra": "report"},
            {"texto": "Next test", "papel": "rotulo", "desde_palavra": "report"},
            {"texto": "Product first vs. logo first", "papel": "leitura", "desde_palavra": "report"},
        ]),
        "desenho": _nas_duas(
            "O anúncio no feed à esquerda e o relatório vazio à direita; em «Upload», pontos correm de um para o "
            "outro e o endereço em mono ganha o sublinhado no grifo; em «report», a leitura e o próximo teste "
            "aparecem no lugar do esqueleto. O endereço está inteiro desde o primeiro quadro."
        ),
    },
}


def conferir_proibido() -> None:
    """Para tudo se alguma fala casa com uma linha do proibido.txt (como `grep -ciE -f $PROIBIDO`).

    A mensagem nunca repete a linha que casou: nenhuma saída usa o que está no arquivo.
    """
    if not PROIBIDO.is_file() or PROIBIDO.stat().st_size == 0:
        raise SystemExit(f"falta o {PROIBIDO} (bloco 3 do docs/ROADMAP.md); sem ele, nenhuma fala vira voz")
    padroes = [linha.strip() for linha in PROIBIDO.read_text(encoding="utf-8").splitlines() if linha.strip()]
    for chave, fala in FALAS.items():
        for campo in ("texto", "voz"):
            for padrao in padroes:
                if re.search(padrao, fala[campo], re.IGNORECASE):
                    raise SystemExit(f"a fala {chave} ({campo}) casa com uma linha do proibido.txt; nada foi gerado")
        for item in (i for itens in fala["tela"].values() for i in itens):
            for padrao in padroes:
                if re.search(padrao, item["texto"], re.IGNORECASE):
                    raise SystemExit(f"o texto de tela da fala {chave} casa com uma linha do proibido.txt")
