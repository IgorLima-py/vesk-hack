"""Confere a variante de fora: decodifica pelo ffmpeg direto, sem importar nada de variante/.

Precisa do ffmpeg com o filtro flite no PATH, porque o E1 sai do gerador sintético (exemplos/README.md).
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
LARGURA, ALTURA, FPS = 720, 1280, 30
MARCA_EM = 4  # o E1
QUADRO_DA_MARCA = MARCA_EM * FPS
QUADROS_DO_TRECHO = FPS  # o 1º segundo


def _python(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", *args], cwd=RAIZ, capture_output=True, text=True)


def _gerar(video: Path, pasta: Path) -> None:
    feito = _python("variante", "gerar", "--video", str(video), "--marca-em", str(MARCA_EM),
                    "--mudanca", "marca_no_inicio", "--saida", str(pasta))
    assert feito.returncode == 0, feito.stderr


def _hashes(video: Path) -> list[str]:
    """O sha256 de cada quadro decodificado em yuv420p, um por vez."""
    tamanho = LARGURA * ALTURA * 3 // 2
    proc = subprocess.Popen([shutil.which("ffmpeg"), "-v", "error", "-i", str(video), "-map", "0:v:0",
                             "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"],
                            stdout=subprocess.PIPE)
    hashes = []
    while quadro := proc.stdout.read(tamanho):
        assert len(quadro) == tamanho
        hashes.append(hashlib.sha256(quadro).hexdigest())
    assert proc.wait() == 0
    return hashes


def _forma(video: Path) -> tuple:
    saida = subprocess.run([shutil.which("ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height:format=duration", "-of", "json", str(video)],
                           capture_output=True, text=True, check=True).stdout
    d = json.loads(saida)
    return d["streams"][0]["width"], d["streams"][0]["height"], d["format"]["duration"]


@pytest.fixture(scope="module")
def e1(tmp_path_factory) -> Path:
    assert shutil.which("ffmpeg"), "ffmpeg não está no PATH"
    video = tmp_path_factory.mktemp("e1") / "e1.mp4"
    feito = _python("exemplos.sintetico", "--marca-em", str(MARCA_EM), "--semente", "1", "--saida", str(video))
    assert feito.returncode == 0, feito.stderr
    return video


@pytest.fixture(scope="module")
def variante(e1, tmp_path_factory) -> Path:
    pasta = tmp_path_factory.mktemp("variante")
    _gerar(e1, pasta)
    return pasta


def _conferir(pasta: Path) -> subprocess.CompletedProcess:
    return _python("variante", "conferir", str(pasta))


def test_variante_uma_mudanca(e1, variante, tmp_path):
    """evita: uma variante que mexe fora do 1º segundo, que não põe a marca nele ou que muda de tamanho."""
    original, nova = _hashes(e1), _hashes(variante / "variante.mp4")
    assert len(original) == len(nova) == 15 * FPS
    assert nova[QUADROS_DO_TRECHO:] == original[QUADROS_DO_TRECHO:]
    assert all(h == original[QUADRO_DA_MARCA] for h in nova[:QUADROS_DO_TRECHO])
    assert nova[15] != original[15]
    assert _forma(e1) == _forma(variante / "variante.mp4")

    cert = json.loads((variante / "certificado.json").read_text(encoding="utf-8"))
    assert cert["trecho"]["inicio"] == 0 and cert["trecho"]["quadro_fim"] == QUADROS_DO_TRECHO
    assert cert["quadro_da_marca"]["n"] == QUADRO_DA_MARCA
    assert Path(cert["original"]["caminho"]) == e1.resolve()

    feito = _conferir(variante)
    assert feito.returncode == 0, feito.stdout + feito.stderr

    _gerar(e1, tmp_path / "de-novo")
    assert (tmp_path / "de-novo" / "variante.mp4").read_bytes() == (variante / "variante.mp4").read_bytes()


def test_certificado_pega_mudanca_fora(variante, tmp_path):
    """evita: um quadro mexido fora do trecho declarado passar pela conferência."""
    pasta = tmp_path / "mexida"
    shutil.copytree(variante, pasta)
    alvo = pasta / "variante.mp4"
    mexida = tmp_path / "mexida.mp4"
    subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-y", "-i", str(alvo),
                    "-vf", "drawbox=x=0:y=0:w=64:h=64:color=red:t=fill:enable='eq(n,200)'",
                    "-c:v", "libx264", "-qp", "0", "-pix_fmt", "yuv420p", "-c:a", "copy", str(mexida)], check=True)
    mexida.replace(alvo)
    hashes = _hashes(alvo)
    assert hashes[200] != _hashes(variante / "variante.mp4")[200]

    feito = _conferir(pasta)
    assert feito.returncode != 0
    assert "quadro 200" in feito.stdout, feito.stdout


def test_certificado_pega_copia(e1, variante, tmp_path):
    """evita: uma cópia do original, com um certificado que declara mudança, passar como variante."""
    pasta = tmp_path / "copia"
    shutil.copytree(variante, pasta)
    shutil.copyfile(e1, pasta / "variante.mp4")
    caminho = pasta / "certificado.json"
    cert = json.loads(caminho.read_text(encoding="utf-8"))
    cert["variante"]["sha256"] = hashlib.sha256((pasta / "variante.mp4").read_bytes()).hexdigest()  # o disfarce
    caminho.write_text(json.dumps(cert, ensure_ascii=False, indent=2), encoding="utf-8")

    feito = _conferir(pasta)
    assert feito.returncode != 0
    assert "cópia" in feito.stdout, feito.stdout
