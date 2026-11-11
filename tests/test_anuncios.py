"""A parte comum dos anúncios (anuncios/), em Python puro: roda no CI sem kokoro, sem whisper e sem ffmpeg."""

from __future__ import annotations

import itertools
import json

import pytest

from anuncios.caminhos import PACOTE
from anuncios.falas import CHAVES, FALAS
from anuncios.tempo import montar
from anuncios.transcrever import alinhar

OUVIDAS = [(" Vesque.", 0.10, 0.52), (" The", 0.70, 0.81), (" creative", 0.81, 1.25), (" autopilot.", 1.25, 1.98)]


# evita: a marca escrita como o whisper ouviu («Vesque») na legenda e no gabarito, e palavra que a voz não disse
def test_alinhar_fala_usa_grafia_do_roteiro():
    palavras = alinhar("Vesk. The creative autopilot.", OUVIDAS)
    assert [p["texto"] for p in palavras] == ["Vesk.", "The", "creative", "autopilot."]
    assert [(p["inicio"], p["fim"]) for p in palavras] == [(0.1, 0.52), (0.7, 0.81), (0.81, 1.25), (1.25, 1.98)]
    with pytest.raises(ValueError, match=r"faltam \['autopilot\.'\]"):
        alinhar("Vesk. The creative autopilot.", OUVIDAS[:3])
    with pytest.raises(ValueError, match=r"sobram \['now'\]"):
        alinhar("Vesk. The creative autopilot.", OUVIDAS + [(" now", 2.0, 2.2)])


def _falas_sinteticas() -> dict[str, dict]:
    falas = {}
    for i, chave in enumerate(CHAVES):
        palavras = FALAS[chave]["texto"].split()
        duracao = 1.0 + 0.37 * i  # durações diferentes e fora do quadro, para o arredondamento aparecer
        passo = (duracao - 0.2) / len(palavras)
        falas[chave] = {"duracao": duracao,
                        "palavras": [{"texto": p, "inicio": round(0.1 + j * passo, 3),
                                      "fim": round(0.1 + (j + 1) * passo, 3)} for j, p in enumerate(palavras)]}
    return falas


def _params(anuncio: str) -> dict:
    params = json.loads((PACOTE / f"{anuncio}.json").read_text(encoding="utf-8"))
    # valores só do teste: os do anúncio são decisão do Igor, e o teste não depende deles
    params.update(pausa_antes_s=0.2, pausa_depois_s=0.3, logo_sonoro_s=0.5)
    return params


# evita: um gabarito cujo marca_em não é o quadro em que a cartela entra, e corte que não é o começo de um segmento
def test_marca_em_e_cortes_saem_da_ordem():
    falas = _falas_sinteticas()
    a, b = montar(_params("a"), falas), montar(_params("b"), falas)
    assert a["quadros"] == b["quadros"]
    for linha in (a, b):
        segmentos = linha["segmentos"]
        assert linha["cortes"] == [s["inicio"] for s in segmentos[1:]]
        assert all(s["fim"] == seguinte["inicio"] for s, seguinte in zip(segmentos, segmentos[1:]))
        antes = list(itertools.takewhile(lambda s: s["chave"] != "marca", segmentos))
        assert linha["marca_em"] == sum(s["fim"] - s["inicio"] for s in antes)
        marca = next(s for s in segmentos if s["chave"] == "marca")
        # o logo sonoro toca no marca_em, e a voz da marca entra depois dele e da pausa
        assert marca["voz_inicio_amostra"] == marca["inicio"] * 800 + round((0.2 + 0.5) * 24000)
    assert b["marca_em"] < a["marca_em"]
