"""Prova que o teste de contrato pega cada falha: roda tests/test_contrato.py contra o motor falso, honesto e adulterado."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
# Valores de teste do motor falso, nunca os do motor real.
CREDENCIAIS = {"MOTOR_KEY": "chave-do-motor-falso", "MOTOR_SECRET": "segredo-do-motor-falso"}


def _rodar_contrato(adulterar: str | None) -> subprocess.CompletedProcess:
    ambiente = {**os.environ, **CREDENCIAIS}
    cmd = [sys.executable, str(RAIZ / "tests" / "motor_falso.py"), "--porta", "0"]
    if adulterar:
        cmd += ["--adulterar", adulterar]
    motor = subprocess.Popen(cmd, env=ambiente, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        linha = motor.stdout.readline()
        achou = re.search(r"http://127\.0\.0\.1:\d+", linha)
        assert achou, f"o motor falso não subiu: {linha!r} {motor.stderr.read() if motor.poll() is not None else ''}"
        return subprocess.run([sys.executable, "-m", "pytest", "tests/test_contrato.py", "-q", "-rs",
                               "-p", "no:cacheprovider"],
                              cwd=RAIZ, env={**ambiente, "MOTOR_URL": achou.group(0)},
                              capture_output=True, text=True, timeout=600)
    finally:
        motor.kill()
        motor.wait()


def test_motor_falso_pega_cada_adulteracao():
    honesto = _rodar_contrato(None)
    assert honesto.returncode == 0, honesto.stdout[-3000:]
    assert "skipped" not in honesto.stdout.lower(), honesto.stdout[-3000:]

    for adulterar in ("sem_request_id", "200_sem_token", "401_com_token"):
        feito = _rodar_contrato(adulterar)
        assert feito.returncode != 0, f"o teste de contrato não pegou --adulterar {adulterar}:\n{feito.stdout[-3000:]}"
        assert "failed" in feito.stdout.lower(), feito.stdout[-3000:]
