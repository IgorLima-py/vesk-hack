"""A linha do tempo de um anúncio (anuncios/linha_do_tempo/<a|b>.json): a única entrada dos motores.

Tudo em quadros, menos o que tem `_s` (segundos) ou `_amostra` (amostras de áudio) no nome. Cada segmento é a pausa
antes, mais o bruto inteiro (sem cortar silêncio, para não ter limiar sem fonte), mais a pausa depois, arredondado
para cima em quadros. Na cartela da marca, o logo sonoro toca no primeiro quadro, e a voz entra depois dele.
Os cortes são o começo de cada segmento, menos o primeiro, e o `marca_em` é o primeiro quadro da cartela.
"""

from __future__ import annotations

import json
import math

from anuncios.caminhos import FALA, LINHA, parametros
from anuncios.falas import CHAVE_DA_MARCA, CHAVES, FALAS

VERSAO = 1
QUEBRA_DA_LEGENDA = (",", ".", "?", "!", ";", ":")  # a legenda quebra na pontuação do roteiro, e só nela


def _quadros(segundos: float, fps: int) -> int:
    return math.ceil(round(segundos * fps, 6))


def _palavra(palavras: list[dict], texto: str) -> dict:
    for p in palavras:
        if p["texto"].strip(".,?!;:") == texto:
            return p
    raise ValueError(f"a palavra {texto!r} não está na fala")


def _legendas(seg: dict) -> list[dict]:
    blocos: list[list[dict]] = []
    atual: list[dict] = []
    for p in seg["palavras"]:
        atual.append(p)
        if p["texto"].endswith(QUEBRA_DA_LEGENDA):
            blocos.append(atual)
            atual = []
    if atual:
        blocos.append(atual)
    legendas = []
    for i, bloco in enumerate(blocos):
        fim = blocos[i + 1][0]["inicio"] if i + 1 < len(blocos) else seg["fim"]
        legendas.append({"texto": " ".join(p["texto"] for p in bloco), "inicio": bloco[0]["inicio"], "fim": fim,
                         "chave": seg["chave"]})
    return legendas


def montar(params: dict, falas: dict[str, dict]) -> dict:
    """A linha do tempo, a partir dos parâmetros do anúncio e do tempo de cada fala (anuncios/fala/<chave>.json)."""
    fps = params["fps"]
    taxa = params["taxa_do_som"]
    if taxa % fps:
        raise ValueError(f"a taxa do som ({taxa}) precisa ser múltipla do fps ({fps}), para o quadro cair numa amostra")
    for nome in ("pausa_antes_s", "pausa_depois_s", "logo_sonoro_s"):
        if params.get(nome) is None:
            raise ValueError(f"{nome} está vazio nos parâmetros: o valor é decisão do Igor e ainda não veio")
    ordem = list(params["ordem"])
    if sorted(ordem) != sorted(CHAVES):
        raise ValueError(f"a ordem precisa ter as seis falas uma vez cada: {ordem}")
    sem_legenda = set(params["legenda"]["sem_legenda"])

    q = 0
    segmentos = []
    for chave in ordem:
        fala = falas[chave]
        antes = params["pausa_antes_s"] + (params["logo_sonoro_s"] if chave == CHAVE_DA_MARCA else 0)
        n = _quadros(antes + fala["duracao"] + params["pausa_depois_s"], fps)
        voz_amostra = q * (taxa // fps) + round(antes * taxa)
        voz_s = voz_amostra / taxa
        palavras = []
        for p in fala["palavras"]:
            inicio = min(max(round((voz_s + p["inicio"]) * fps), q), q + n - 1)
            fim = min(max(round((voz_s + p["fim"]) * fps), inicio + 1), q + n)
            palavras.append({"texto": p["texto"], "inicio": inicio, "fim": fim})
        tela = []
        for item in FALAS[chave]["tela"]:
            if item["papel"] == "frase_palavra_a_palavra":
                inicio = palavras[0]["inicio"]
            elif "desde_palavra" in item:
                inicio = _palavra(palavras, item["desde_palavra"])["inicio"]
            else:
                inicio = q
            tela.append({**item, "inicio": inicio, "fim": q + n})
        segmentos.append({
            "chave": chave,
            "inicio": q,
            "fim": q + n,
            "texto": FALAS[chave]["texto"],
            "fala_inicio_s": round(voz_s + fala["palavras"][0]["inicio"], 3),
            "fala_fim_s": round(voz_s + fala["palavras"][-1]["fim"], 3),
            "voz_inicio_amostra": voz_amostra,
            "palavras": palavras,
            "tela": tela,
            "legenda": chave not in sem_legenda,
            "desenho": FALAS[chave]["desenho"],
        })
        q += n

    marca = next(s for s in segmentos if s["chave"] == CHAVE_DA_MARCA)
    legendas = [leg for s in segmentos if s["legenda"] for leg in _legendas(s)]
    textos = sorted([{"texto": t["texto"], "inicio": t["inicio"], "fim": t["fim"]} for s in segmentos for t in s["tela"]]
                    + [{"texto": leg["texto"], "inicio": leg["inicio"], "fim": leg["fim"]} for leg in legendas],
                    key=lambda t: (t["inicio"], t["texto"]))
    return {
        "versao": VERSAO,
        "fps": fps,
        "largura": params["largura"],
        "altura": params["altura"],
        "quadros": q,
        "taxa_do_som": taxa,
        "marca_em": marca["inicio"],
        "cortes": [s["inicio"] for s in segmentos[1:]],
        "logo_sonoro_s": params["logo_sonoro_s"],
        "visual": params["visual"],
        "zona_segura": params["zona_segura"],
        "cartela_marca": params["cartela_marca"],
        "legenda": params["legenda"],
        "segmentos": segmentos,
        "legendas": legendas,
        "textos": textos,
    }


def ler_falas() -> dict[str, dict]:
    return {c: json.loads((FALA / f"{c}.json").read_text(encoding="utf-8")) for c in CHAVES}


def main(anuncio: str) -> int:
    params = json.loads(parametros(anuncio).read_text(encoding="utf-8"))
    try:
        linha = montar(params, ler_falas())
    except ValueError as erro:
        print(f"erro: {erro}")
        return 2
    LINHA.mkdir(parents=True, exist_ok=True)
    saida = LINHA / f"{anuncio}.json"
    saida.write_text(json.dumps(linha, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fps = linha["fps"]
    print(f"{saida}: {linha['quadros']} quadros ({linha['quadros'] / fps:.3f} s), marca_em no quadro "
          f"{linha['marca_em']} ({linha['marca_em'] / fps:.3f} s), cortes {linha['cortes']}")
    return 0
