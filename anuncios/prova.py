"""As medidas de uma frente da prova dos motores, iguais para todas ($VIDEOS/provas/<motor>/medidas.json).

    python -m anuncios prova <motor> --render <mp4 1> --render <mp4 2> --projeto <pasta> [--pacote <npm>]

Cada render é a imagem muda do A, desenhada a partir de anuncios/linha_do_tempo/a.json. A prova mede:
1. se os dois renders dão o mesmo `framemd5` (quadro a quadro);
2. se a cartela entra no quadro do `marca_em`: mais da metade do miolo da barra está no grifo nesse quadro, e menos
   da metade no anterior;
3. o tamanho, o fps e o número de quadros, contra a linha do tempo;
4. as linhas de código do projeto (sem node_modules, lock, saída de build);
5. a licença do pacote do motor, com o trecho.
O tempo de render e o pico de RAM vêm da fila (gpu_job), e o que travou vem do relato de quem montou a frente.
Os cortes que o ffmpeg vê (scene > 0,3, o limiar dos testes do sintético da C3) saem como informação.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from anuncios.caminhos import LINHA, PROVAS
from anuncios.final import _sonda

TOLERANCIA_COR = 24  # por canal, a mesma dos testes do sintético da C3: o yuv420p mexe um pouco na cor
MIOLO = 2  # px tirados de cada lado da barra: o yuv420p subamostra o croma em 2x2, e a borda mistura as cores
# A barra está ou não está: presente é mais da metade do miolo no grifo, o ponto do meio entre ausente (0) e presente
# (1). Exigir 1,0 exato reprovou a Remotion por 6 a 8 px de ruído de croma do h264 nos cantos (0,999 no marca_em e 0,0
# no quadro anterior, jobs 1300 e 1306, 11/11/2026).
PRESENTE = 0.5
LIMIAR_DE_CENA = 0.3  # o mesmo dos testes do sintético da C3
EXTENSOES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".html", ".css", ".py", ".vue", ".svelte", ".wgsl"}
FORA = {"node_modules", "dist", "out", "build", ".cache", "output", "renders"}


def _ffmpeg() -> str:
    caminho = shutil.which("ffmpeg")
    if not caminho:
        raise SystemExit("ffmpeg não encontrado no PATH")
    return caminho


def framemd5(video: Path) -> tuple[str, int]:
    saida = subprocess.run([_ffmpeg(), "-v", "error", "-i", str(video), "-map", "0:v", "-f", "framemd5", "-"],
                           capture_output=True, text=True, check=True).stdout
    quadros = [linha for linha in saida.splitlines() if linha and not linha.startswith("#")]
    return hashlib.sha256("\n".join(quadros).encode()).hexdigest(), len(quadros)


def quadro_rgb(video: Path, n: int) -> bytes:
    return subprocess.run([_ffmpeg(), "-v", "error", "-i", str(video), "-vf", f"select=eq(n\\,{n})",
                           "-fps_mode", "passthrough", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          capture_output=True, check=True).stdout


def barra_no_grifo(rgb: bytes, largura: int, barra: dict, grifo: str) -> float:
    """A fração do miolo da barra que está no grifo (1.0 é a barra inteira)."""
    r, g, b = (int(grifo[i:i + 2], 16) for i in (1, 3, 5))
    x0, y0 = barra["x"] + MIOLO, barra["y"] + MIOLO
    x1, y1 = barra["x"] + barra["largura"] - MIOLO, barra["y"] + barra["altura"] - MIOLO
    total = dentro = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = (y * largura + x) * 3
            total += 1
            if (abs(rgb[i] - r) <= TOLERANCIA_COR and abs(rgb[i + 1] - g) <= TOLERANCIA_COR
                    and abs(rgb[i + 2] - b) <= TOLERANCIA_COR):
                dentro += 1
    return dentro / total


def cortes_vistos(video: Path, fps: int) -> list[int]:
    saida = subprocess.run([_ffmpeg(), "-hide_banner", "-i", str(video), "-vf",
                            f"select='gt(scene,{LIMIAR_DE_CENA})',showinfo", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    return [round(float(t) * fps) for t in re.findall(r"pts_time:([0-9.]+)", saida)]


def linhas_de_codigo(projeto: Path) -> dict:
    por_arquivo = {}
    for arquivo in sorted(projeto.rglob("*")):
        partes = set(arquivo.relative_to(projeto).parts[:-1])
        if not arquivo.is_file() or arquivo.suffix not in EXTENSOES or partes & FORA:
            continue
        texto = arquivo.read_text(encoding="utf-8", errors="replace")
        por_arquivo[arquivo.relative_to(projeto).as_posix()] = sum(1 for linha in texto.splitlines() if linha.strip())
    return {"total": sum(por_arquivo.values()), "arquivos": por_arquivo}


def licenca(projeto: Path, pacote: str | None) -> dict:
    if not pacote:
        return {"pacote": None}
    pasta = projeto / "node_modules" / pacote
    info = {"pacote": pacote}
    manifesto = pasta / "package.json"
    if manifesto.is_file():
        dados = json.loads(manifesto.read_text(encoding="utf-8"))
        info.update({"versao": dados.get("version"), "licenca": dados.get("license")})
    arquivos = sorted(pasta.glob("LICEN[CS]E*"))
    if arquivos:
        info["arquivo"] = arquivos[0].name
        info["trecho"] = arquivos[0].read_text(encoding="utf-8", errors="replace").strip()[:400]
    return info


def main(motor: str, renders: list[Path], projeto: Path, pacote: str | None = None,
         caminho_da_linha: Path | None = None) -> int:
    linha = json.loads(Path(caminho_da_linha or LINHA / "a.json").read_text(encoding="utf-8"))
    if len(renders) != 2:
        raise SystemExit("passe dois renders (--render duas vezes)")
    sondas = [_sonda(r) for r in renders]
    md5s = [framemd5(r) for r in renders]
    n = linha["marca_em"]
    barra, grifo = linha["cartela_marca"]["barra"], linha["visual"]["grifo"]
    no_marca_em = barra_no_grifo(quadro_rgb(renders[0], n), linha["largura"], barra, grifo)
    antes = barra_no_grifo(quadro_rgb(renders[0], n - 1), linha["largura"], barra, grifo)
    medidas = {
        "motor": motor,
        "mesmo_framemd5": md5s[0][0] == md5s[1][0],
        "framemd5_sha256": [m[0] for m in md5s],
        "formato_bate": all(s["largura"] == linha["largura"] and s["altura"] == linha["altura"]
                            and s["fps"] == linha["fps"] and s["quadros"] == linha["quadros"] for s in sondas),
        "sondas": [{**s, "fps": str(s["fps"])} for s in sondas],
        "quadros_esperados": linha["quadros"],
        "marca_em": n,
        "barra_no_marca_em": round(no_marca_em, 4),
        "barra_no_quadro_anterior": round(antes, 4),
        "cartela_no_quadro_certo": no_marca_em > PRESENTE and antes < PRESENTE,
        "cortes_esperados": linha["cortes"],
        "cortes_vistos": cortes_vistos(renders[0], linha["fps"]),
        "linhas_de_codigo": linhas_de_codigo(projeto),
        "licenca": licenca(projeto, pacote),
    }
    pasta = PROVAS / motor
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "medidas.json").write_text(json.dumps(medidas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    resumo = {k: medidas[k] for k in ("mesmo_framemd5", "formato_bate", "cartela_no_quadro_certo",
                                      "barra_no_marca_em", "barra_no_quadro_anterior", "cortes_vistos")}
    print(json.dumps({"motor": motor, **resumo, "linhas_de_codigo": medidas["linhas_de_codigo"]["total"],
                      "licenca": medidas["licenca"].get("licenca")}, ensure_ascii=False))
    return 0 if medidas["mesmo_framemd5"] and medidas["formato_bate"] and medidas["cartela_no_quadro_certo"] else 1
