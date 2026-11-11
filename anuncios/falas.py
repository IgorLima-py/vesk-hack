"""O roteiro dos anúncios A e B: seis falas em inglês, para o público dos EUA (plano aprovado pelo Igor em 11/11/2026).

Cada fala tem:
- `texto`: a grafia, que vai para a legenda e para o gabarito;
- `voz`: o que o Kokoro lê. É o mesmo texto, com a pronúncia fixada onde o inglês é ambíguo ou a palavra é nossa;
- `tela`: o texto que o motor escreve na tela (sem número nenhum);
- `desenho`: o que o motor desenha no segmento, igual para todos os motores da prova.
"""

from __future__ import annotations

import re

from anuncios.caminhos import PROIBIDO

CHAVES = ("gancho", "problema", "leitura", "variante", "marca", "chamada")
CHAVE_DA_MARCA = "marca"

FALAS: dict[str, dict] = {
    "gancho": {
        "texto": "Your ad is losing people in the first seconds.",
        "voz": "Your ad is losing people in the first seconds.",
        "tela": [{"texto": "Your ad is losing people in the first seconds.", "papel": "frase_palavra_a_palavra"}],
        "desenho": (
            "A frase entra palavra a palavra, cada palavra no quadro em que é dita (segmento.palavras), em serifa "
            "(Newsreader), na cor do texto, no terço de cima da zona segura. Embaixo dela, uma curva de retenção "
            "desenhada como ilustração (uma linha só, na cor do texto) cai da esquerda para a direita enquanto o "
            "segmento corre. Sem eixo, sem rótulo, sem número."
        ),
    },
    "problema": {
        "texto": "You can see when they leave. Not why.",
        "voz": "You can see when they leave. Not why.",
        "tela": [{"texto": "?", "papel": "interrogacao", "desde_palavra": "Not"}],
        "desenho": (
            "A curva inteira, parada, e o ponto onde ela despenca marcado por um círculo no grifo. Ao lado do ponto, "
            "um «?» grande em serifa, na cor do grifo, entra na primeira palavra de «Not why.». Sem número."
        ),
    },
    "leitura": {
        "texto": "We read your video, second by second, and match it to the moment people drop off.",
        "voz": "We [read](/ɹˈid/) your video, second by second, and match it to the moment people drop off.",
        "tela": [],
        "desenho": (
            "A curva no alto e, embaixo dela, uma tira horizontal de quadros (retângulos com composições abstratas, "
            "na cor do cartão, com borda) correndo da direita para a esquerda. Uma linha vertical no grifo percorre "
            "a curva e a tira juntas, da esquerda para a direita, durante o segmento, e para no ponto da queda. Sem "
            "texto."
        ),
    },
    "variante": {
        "texto": "Then you get a variant with one change, ready to test.",
        "voz": "Then you get a variant with one change, ready to test.",
        "tela": [],
        "desenho": (
            "Dois quadros verticais lado a lado, iguais, de um anúncio abstrato (retângulos e um círculo na cor do "
            "texto, sobre o cartão). No da direita, um elemento só aparece trocado e contornado no grifo, a partir "
            "da palavra «one». Sem texto."
        ),
    },
    "marca": {
        "texto": "Vesk. The creative autopilot.",
        "voz": "[Vesk](/vˈɛsk/). The creative autopilot.",
        "tela": [
            {"texto": "Vesk", "papel": "wordmark"},
            {"texto": "The creative autopilot.", "papel": "assinatura"},
        ],
        "desenho": (
            "A cartela da marca: fundo preto; o wordmark «Vesk» em Newsreader peso 500, na cor do texto, centrado, "
            "logo acima da barra; a barra do grifo (a mesma do h1 do site) ocupa exatamente o retângulo "
            "cartela_marca.barra; e «The creative autopilot.» em Schibsted Grotesk, na cor mudo, logo abaixo dela. "
            "Tudo entra inteiro no primeiro quadro do segmento, que é o marca_em, sem animação de entrada. Nada no "
            "grifo pode ocupar o retângulo da barra antes desse quadro."
        ),
    },
    "chamada": {
        "texto": "Upload your ad. Get the report.",
        "voz": "Upload your ad. Get the report.",
        "tela": [{"texto": "hack.vesklab.com", "papel": "endereco"}],
        "desenho": (
            "A cartela final: «hack.vesklab.com» em IBM Plex Mono, na cor do texto, centrado, sublinhado no grifo. "
            "A legenda queimada traz a frase; o motor só escreve o endereço."
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
        for item in fala["tela"]:
            for padrao in padroes:
                if re.search(padrao, item["texto"], re.IGNORECASE):
                    raise SystemExit(f"o texto de tela da fala {chave} casa com uma linha do proibido.txt")
