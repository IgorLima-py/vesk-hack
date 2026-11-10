"""Confere o gerador sintético de fora: pelo ffmpeg e pelo ffprobe, sem usar nada de exemplos/ além da linha de comando."""

from __future__ import annotations

import array
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TOLERANCIA_COR = 24  # por canal: o yuv420p mexe um pouco na cor das bordas


def _ffmpeg(nome: str) -> str:
    caminho = shutil.which(nome)
    assert caminho, f"{nome} não está no PATH; os testes do sintético precisam do ffmpeg com o filtro flite"
    return caminho


def _gerar(saida: Path, *args: str) -> dict:
    feito = subprocess.run([sys.executable, "-m", "exemplos.sintetico", "--saida", str(saida), *args],
                           cwd=RAIZ, capture_output=True, text=True)
    assert feito.returncode == 0, feito.stderr
    return json.loads((saida.parent / "gabarito.json").read_text(encoding="utf-8"))


def _streams(video: Path) -> tuple[list[str], float]:
    saida = subprocess.run([_ffmpeg("ffprobe"), "-v", "error", "-show_entries", "stream=codec_type:format=duration",
                            "-of", "json", str(video)], capture_output=True, text=True, check=True).stdout
    dados = json.loads(saida)
    return sorted(s["codec_type"] for s in dados["streams"]), float(dados["format"]["duration"])


def _trocas_de_cena(video: Path) -> list[float]:
    saida = subprocess.run([_ffmpeg("ffmpeg"), "-hide_banner", "-i", str(video), "-vf",
                            "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    return [float(t) for t in re.findall(r"pts_time:([0-9.]+)", saida)]


def _pixels_da_cor(video: Path, t: float, cor: list[int], largura: int, altura: int) -> int:
    cru = subprocess.run([_ffmpeg("ffmpeg"), "-v", "error", "-ss", f"{t}", "-i", str(video), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    assert len(cru) == largura * altura * 3
    r, g, b = cor
    return sum(1 for i in range(0, len(cru), 3)
               if abs(cru[i] - r) <= TOLERANCIA_COR and abs(cru[i + 1] - g) <= TOLERANCIA_COR
               and abs(cru[i + 2] - b) <= TOLERANCIA_COR)


def _audio(video: Path, taxa: int = 16000) -> array.array:
    cru = subprocess.run([_ffmpeg("ffmpeg"), "-v", "error", "-i", str(video), "-f", "s16le", "-ac", "1",
                          "-ar", str(taxa), "-"], capture_output=True, check=True).stdout
    amostras = array.array("h", cru)
    if sys.byteorder == "big":
        amostras.byteswap()
    return amostras


def _rms(amostras) -> float:
    return (sum(a * a for a in amostras) / max(1, len(amostras))) ** 0.5


def test_sintetico_gabarito(tmp_path):
    video = tmp_path / "com" / "v.mp4"
    g = _gerar(video, "--marca-em", "3", "--semente", "5", "--duracao", "8")

    assert g["marca_em"] == 3 and g["semente"] == 5 and g["duracao"] == 8
    assert set(g) >= {"marca_em", "cortes", "fala", "texto", "cor_do_texto", "duracao", "semente"}
    assert g["video_sha256"] == hashlib.sha256(video.read_bytes()).hexdigest()

    tipos, duracao = _streams(video)
    assert tipos == ["audio", "video"]
    assert abs(duracao - g["duracao"]) < 0.1

    trocas = _trocas_de_cena(video)
    assert g["cortes"], "a semente 5 com 8 s tem de dar pelo menos um corte"
    assert len(trocas) == len(g["cortes"]), (trocas, g["cortes"])
    assert all(abs(a - b) <= 0.1 for a, b in zip(trocas, g["cortes"])), (trocas, g["cortes"])

    w, h, cor = g["largura"], g["altura"], g["cor_do_texto"]
    assert _pixels_da_cor(video, g["marca_em"] - 0.5, cor, w, h) == 0
    assert _pixels_da_cor(video, g["marca_em"] + 0.5, cor, w, h) >= 500
    assert g["texto"] == [{"texto": "VESK", "inicio": 3, "fim": 8}]

    assert [f["tem_marca"] for f in g["fala"]].count(True) == 1
    marca = next(f for f in g["fala"] if f["tem_marca"])
    assert marca["inicio"] == g["marca_em"] and marca["texto"].startswith("Vesk")
    taxa = 16000
    som = _audio(video, taxa)
    fora = [a for i, a in enumerate(som)
            if not any(f["inicio"] - 0.2 <= i / taxa <= f["fim"] + 0.2 for f in g["fala"])]
    silencio = _rms(fora)
    for f in g["fala"]:
        dentro = som[int(f["inicio"] * taxa):int(f["fim"] * taxa)]
        assert _rms(dentro) > 10 * (silencio + 1), (f, _rms(dentro), silencio)

    sem = tmp_path / "sem" / "v.mp4"
    g2 = _gerar(sem, "--marca-em", "3", "--semente", "5", "--duracao", "8", "--sem-marca")
    assert g2["marca_em"] is None and g2["texto"] == []
    assert not any(f["tem_marca"] for f in g2["fala"])
    assert _pixels_da_cor(sem, 2.5, cor, w, h) == 0
    assert _pixels_da_cor(sem, 3.5, cor, w, h) == 0


def test_mesma_semente_mesmo_video(tmp_path):
    def sha(pasta: str, semente: str) -> str:
        video = tmp_path / pasta / "v.mp4"
        _gerar(video, "--marca-em", "2", "--semente", semente, "--duracao", "5")
        return hashlib.sha256(video.read_bytes()).hexdigest()

    primeira = sha("a", "7")
    assert sha("b", "7") == primeira
    assert sha("c", "8") != primeira
