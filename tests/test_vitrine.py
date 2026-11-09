"""Evita publicar a vitrine quebrada: as duas paginas existem, tem o idioma certo,
a frase da trilha, tamanho minimo e nenhum formulario (a pagina nao coleta nada)."""
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "site" / "public"


def _ler(nome):
    return (PUBLIC / nome).read_text(encoding="utf-8")


def test_vitrine_paginas_sem_formulario_e_no_idioma():
    en, pt = _ler("index.html"), _ler("pt.html")
    assert '<html lang="en"' in en and "creative autopilot" in en.lower()
    assert '<html lang="pt-BR"' in pt and "piloto automático do criativo" in pt.lower()
    assert len(en.encode()) >= 1500 and len(pt.encode()) >= 1500
    assert en != pt
    for corpo in (en, pt):
        assert "<form" not in corpo.lower()
