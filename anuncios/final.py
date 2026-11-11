"""O mp4 final de um anúncio e o gabarito ao lado: a imagem muda do motor, a legenda queimada e o som.

A legenda sai da linha do tempo para um .ass e é queimada pelo filtro `subtitles` do ffmpeg. O ffmpeg roda com a
pasta da montagem como pasta de trabalho, com as fontes copiadas para lá: o caminho do filtro fica sem `C:` para
escapar. As flags `bitexact` são as do exemplos/sintetico.py, e o gabarito tem as chaves do gabarito da C3.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

from anuncios.caminhos import FONTES, LINHA, MONTAGEM, VIDEOS

VERSAO_GABARITO = 1


def _ffmpeg(nome: str = "ffmpeg") -> str:
    caminho = shutil.which(nome)
    if not caminho:
        raise SystemExit(f"{nome} não encontrado no PATH")
    return caminho


def _numero(x: float) -> float | int:
    x = round(float(x), 3)
    return int(x) if x == int(x) else x


def _cor_ass(hexa: str) -> str:
    r, g, b = hexa[1:3], hexa[3:5], hexa[5:7]
    return f"&H00{b}{g}{r}".upper()


def _tempo_ass(quadro: int, fps: int) -> str:
    """O tempo do .ass (centésimos) que cai entre o quadro anterior e este: o evento começa exatamente nele."""
    cs = quadro * 100 // fps
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def ass(linha: dict) -> str:
    leg, zona, fps = linha["legenda"], linha["zona_segura"], linha["fps"]
    cor = _cor_ass(leg["cor"])
    linhas = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {linha['largura']}",
        f"PlayResY: {linha['altura']}",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        f"Style: Legenda,{leg['familia']},{leg['tamanho']},{cor},{cor},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,"
        f"{leg['contorno']},0,2,{zona['lados']},{zona['lados']},{zona['base']},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for item in linha["legendas"]:
        linhas.append(f"Dialogue: 0,{_tempo_ass(item['inicio'], fps)},{_tempo_ass(item['fim'], fps)},Legenda,,0,0,0,,"
                      f"{item['texto']}")
    return "\n".join(linhas) + "\n"


def _sonda(video: Path) -> dict:
    saida = subprocess.run([_ffmpeg("ffprobe"), "-v", "error", "-count_frames", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames", "-of", "json",
                            str(video)], capture_output=True, text=True, check=True).stdout
    s = json.loads(saida)["streams"][0]
    return {"largura": s["width"], "altura": s["height"], "fps": Fraction(s["r_frame_rate"]),
            "quadros": int(s["nb_read_frames"])}


def gabarito(linha: dict, video_sha256: str) -> dict:
    fps = linha["fps"]
    return {
        "versao": VERSAO_GABARITO,
        "duracao": _numero(linha["quadros"] / fps),
        "fps": fps,
        "largura": linha["largura"],
        "altura": linha["altura"],
        "marca_em": _numero(linha["marca_em"] / fps),
        "cortes": [_numero(c / fps) for c in linha["cortes"]],
        "fala": [{"texto": s["texto"], "inicio": s["fala_inicio_s"], "fim": s["fala_fim_s"],
                  "tem_marca": s["chave"] == "marca"} for s in linha["segmentos"]],
        "texto": [{"texto": t["texto"], "inicio": _numero(t["inicio"] / fps), "fim": _numero(t["fim"] / fps)}
                  for t in linha["textos"]],
        "video_sha256": video_sha256,
    }


def main(anuncio: str, imagem: Path, saida: Path | None = None) -> int:
    linha = json.loads((LINHA / f"{anuncio}.json").read_text(encoding="utf-8"))
    pasta = MONTAGEM / anuncio
    som = pasta / "som.wav"
    if not som.is_file():
        raise SystemExit(f"falta o {som}: rode `python -m anuncios som {anuncio}` antes")
    imagem = Path(imagem).resolve()
    sonda = _sonda(imagem)
    esperado = {"largura": linha["largura"], "altura": linha["altura"], "fps": Fraction(linha["fps"]),
                "quadros": linha["quadros"]}
    if sonda != esperado:
        raise SystemExit(f"a imagem do motor não bate com a linha do tempo: {sonda} contra {esperado}")

    fontes = pasta / "fontes"
    fontes.mkdir(parents=True, exist_ok=True)
    for ttf in FONTES.glob("*/*.ttf"):
        shutil.copyfile(ttf, fontes / ttf.name)
    (pasta / "legenda.ass").write_text(ass(linha), encoding="utf-8")

    saida = Path(saida or VIDEOS / f"{anuncio}.mp4").resolve()
    saida.parent.mkdir(parents=True, exist_ok=True)
    feito = subprocess.run([
        _ffmpeg(), "-hide_banner", "-y", "-v", "info",
        "-i", str(imagem), "-i", "som.wav",
        "-filter_complex", "[0:v]subtitles=filename=legenda.ass:fontsdir=fontes,format=yuv420p[v]",
        "-map", "[v]", "-map", "1:a",
        "-frames:v", str(linha["quadros"]), "-r", str(linha["fps"]),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-colorspace", "smpte170m", "-color_primaries", "smpte170m", "-color_trc", "smpte170m",
        "-color_range", "tv",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "1",
        "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
        "-map_metadata", "-1", "-movflags", "+faststart",
        str(saida),
    ], cwd=pasta, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if feito.returncode != 0:
        raise SystemExit(f"o ffmpeg falhou ({feito.returncode}): {feito.stderr[-2000:]}")
    escolhas = re.findall(r"fontselect: \((.*?)\) -> (.*)", feito.stderr)
    familia = linha["legenda"]["familia"]
    if linha["legendas"] and not any(familia.replace(" ", "") in destino.replace(" ", "") for _, destino in escolhas):
        raise SystemExit(f"o libass não usou a {familia} na legenda: {escolhas or 'nenhuma fontselect no log'}")

    sha = hashlib.sha256(saida.read_bytes()).hexdigest()
    g = gabarito(linha, sha)
    (saida.parent / f"{saida.stem}.gabarito.json").write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n",
                                                              encoding="utf-8")
    print(f"{saida} ({g['duracao']} s, marca_em {g['marca_em']} s, sha256 {sha[:12]}); fontes da legenda: {escolhas}")
    return 0
