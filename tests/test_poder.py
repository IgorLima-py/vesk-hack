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


@pytest.mark.parametrize("p1, p2", [("0.05", "0.05"), ("0.5", "0.5000000000000001"),
                                    ("0.3", "0.30000000000000004"), ("0.5", "0.5000001")])
def test_poder_sem_efeito(p1, p2):
    """evita: devolver um n, travar ou cair com traceback quando as taxas são iguais (ou só diferem no float)."""
    feito = subprocess.run([sys.executable, "-m", "teste", "poder", "--p1", p1, "--p2", p2],
                           cwd=RAIZ, capture_output=True, text=True, timeout=20)
    assert feito.returncode != 0
    assert "não há efeito a detectar" in feito.stderr
    assert "Traceback" not in feito.stderr
