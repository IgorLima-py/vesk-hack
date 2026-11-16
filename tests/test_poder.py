"""Confere a calculadora de poder contra o statsmodels, pela linha de comando."""

from __future__ import annotations

import math
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


def _poder(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "teste", "poder", *args], cwd=RAIZ, capture_output=True, text=True)


@pytest.mark.parametrize("p1, p2", [(0.30, 0.33), (0.10, 0.12), (0.50, 0.55), (0.02, 0.025), (0.60, 0.40)])
def test_poder_igual_statsmodels(p1, p2):
    """evita: uma fórmula escrita à mão que se afasta da referência e promete teste curto demais."""
    power = pytest.importorskip("statsmodels.stats.power")
    proportion = pytest.importorskip("statsmodels.stats.proportion")
    esperado = math.ceil(power.NormalIndPower().solve_power(
        proportion.proportion_effectsize(p2, p1), alpha=0.05, power=0.8, ratio=1))
    feito = _poder("--p1", str(p1), "--p2", str(p2), "--alfa", "0.05", "--poder", "0.8")
    assert feito.returncode == 0, feito.stderr
    assert int(re.search(r"^n por braço: (\d+)$", feito.stdout, re.M).group(1)) == esperado
    assert "Cohen" in feito.stdout


def test_poder_sem_efeito():
    """evita: devolver um n (ou infinito) quando as duas taxas são iguais."""
    feito = _poder("--p1", "0.05", "--p2", "0.05")
    assert feito.returncode != 0
    assert "não há efeito a detectar" in feito.stderr
