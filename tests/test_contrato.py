"""O teste de contrato do motor (contrato/motor.md).

Com MOTOR_URL, MOTOR_KEY e MOTOR_SECRET no ambiente, manda o E1 ao motor e confere a
resposta, o 401 sem token, o 415 e a rota de saúde. Sem eles, pula e diz o motivo.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import jsonschema
import pytest
import requests

from exemplos.sintetico import gerar

MOTOR_URL = os.environ.get("MOTOR_URL", "").rstrip("/")
MOTOR_KEY = os.environ.get("MOTOR_KEY", "")
MOTOR_SECRET = os.environ.get("MOTOR_SECRET", "")

pytestmark = pytest.mark.skipif(
    not (MOTOR_URL and MOTOR_KEY and MOTOR_SECRET),
    reason="sem MOTOR_URL (com MOTOR_KEY e MOTOR_SECRET) no ambiente: o teste de contrato precisa do motor",
)

RAIZ = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((RAIZ / "contrato" / "motor.schema.json").read_text(encoding="utf-8"))
ESPERA_S = 300
CABECALHOS = {"Modal-Key": MOTOR_KEY, "Modal-Secret": MOTOR_SECRET}


def _validador(defn: str | None = None) -> jsonschema.Draft202012Validator:
    schema = SCHEMA if defn is None else {"$defs": SCHEMA["$defs"], "$ref": f"#/$defs/{defn}"}
    return jsonschema.Draft202012Validator(schema)


@pytest.fixture(scope="module")
def e1(tmp_path_factory) -> Path:
    video = tmp_path_factory.mktemp("e1") / "e1.mp4"
    gerar(marca_em=4, semente=1, saida=video)
    return video


@pytest.fixture(scope="module")
def resposta(e1):
    with e1.open("rb") as f:
        r = requests.post(f"{MOTOR_URL}/analisar", headers=CABECALHOS, data={"marca": "Vesk"},
                          files={"video": ("e1.mp4", f, "video/mp4")}, timeout=ESPERA_S)
    return r


def test_saude():
    r = requests.get(f"{MOTOR_URL}/saude", headers=CABECALHOS, timeout=60)
    assert r.status_code == 200, r.text[:500]
    _validador("saude").validate(r.json())


def test_analisar_cumpre_o_schema(resposta, e1):
    assert resposta.status_code == 200, resposta.text[:500]
    corpo = resposta.json()
    _validador().validate(corpo)
    assert corpo["video_sha256"] == hashlib.sha256(e1.read_bytes()).hexdigest()


def test_analisar_regras_fora_do_schema(resposta):
    assert resposta.status_code == 200, resposta.text[:500]
    arquivos = resposta.json()["arquivos"]
    segundos = [linha["t"] for linha in arquivos["xt.csv"]]
    assert segundos == list(range(len(segundos))), "o t do xt.csv tem de começar em 0 e subir de 1 em 1"
    palavras = [linha["pts"] for linha in arquivos["eventos.csv"] if linha["evento"] == "palavra"]
    assert palavras == sorted(palavras), "as palavras têm de vir em ordem de pts"


def test_sem_token_da_401(e1):
    assert requests.get(f"{MOTOR_URL}/saude", timeout=60).status_code == 401
    with e1.open("rb") as f:
        r = requests.post(f"{MOTOR_URL}/analisar", data={"marca": "Vesk"},
                          files={"video": ("e1.mp4", f, "video/mp4")}, timeout=ESPERA_S)
    assert r.status_code == 401


def test_texto_no_lugar_do_video_da_415():
    r = requests.post(f"{MOTOR_URL}/analisar", headers=CABECALHOS, data={"marca": "Vesk"},
                      files={"video": ("nota.txt", b"isto nao e um video\n" * 50, "text/plain")}, timeout=ESPERA_S)
    assert r.status_code == 415, r.text[:500]
    _validador("erro").validate(r.json())
