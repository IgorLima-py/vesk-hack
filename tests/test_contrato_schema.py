import json
from pathlib import Path

import jsonschema

CONTRATO = Path(__file__).resolve().parent.parent / "contrato"


def _ler(caminho: Path):
    return json.loads(caminho.read_text(encoding="utf-8"))


def test_contrato_schema_valido():
    schema = _ler(CONTRATO / "motor.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    validador = jsonschema.Draft202012Validator(schema)

    ok = _ler(CONTRATO / "exemplos" / "resposta-ok.json")
    erros = [e.message for e in validador.iter_errors(ok)]
    assert erros == [], erros
    assert len(ok["arquivos"]["manifesto.json"]["camadas"]) == 13

    ruins = sorted((CONTRATO / "exemplos").glob("resposta-ruim-*.json"))
    assert [r.name for r in ruins] == [
        "resposta-ruim-12-camadas.json",
        "resposta-ruim-campo-a-mais.json",
        "resposta-ruim-segundo-texto.json",
        "resposta-ruim-sem-eventos.json",
        "resposta-ruim-sem-request-id.json",
    ]
    aceitas = [r.name for r in ruins if validador.is_valid(_ler(r))]
    assert aceitas == [], f"o schema aceitou respostas ruins: {aceitas}"
