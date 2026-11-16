"""Confere uma variante contra o original, decodificando os dois de novo: o certificado não é tomado como verdade.

Pega a mudança fora do trecho declarado (um quadro qualquer que não bate com o original) e a cópia disfarçada (um
certificado que declara mudança sobre um vídeo em que nada mudou).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from variante import quadros as q
from variante.gerar import ARQUIVO_CERTIFICADO, TRECHO_FIM, TRECHO_INICIO


class CertificadoInvalido(ValueError):
    pass


@dataclass
class Checagem:
    ok: bool
    texto: str


def _amostra(ns: list[int], limite: int = 10) -> str:
    texto = ", ".join(str(n) for n in ns[:limite])
    return texto + (f" e mais {len(ns) - limite}" if len(ns) > limite else "")


def conferir(pasta: Path) -> list[Checagem]:
    pasta = Path(pasta)
    try:
        cert = json.loads((pasta / ARQUIVO_CERTIFICADO).read_text(encoding="utf-8"))
        original = Path(cert["original"]["caminho"])
        variante = pasta / cert["variante"]["arquivo"]
        trecho = cert["trecho"]
        n_marca_cert = int(cert["quadro_da_marca"]["n"])
        fora_cert = {int(f["n"]): f["hash"] for f in cert["fora"]}
    except FileNotFoundError as erro:
        raise CertificadoInvalido(f"não achei {erro.filename}") from erro
    except (KeyError, TypeError, ValueError) as erro:
        raise CertificadoInvalido(f"certificado mal formado em {pasta / ARQUIVO_CERTIFICADO}: {erro!r}") from erro

    r: list[Checagem] = []

    # 1. O original é o que o certificado aponta.
    if not original.is_file():
        r.append(Checagem(False, f"o original {original} não existe"))
        return r
    sha_original = q.sha256_do_arquivo(original)
    r.append(Checagem(sha_original == cert["original"]["sha256"],
                      f"o original {original} tem o sha256 do certificado ({sha_original[:12]})"))
    if not variante.is_file():
        r.append(Checagem(False, f"a variante {variante} não existe"))
        return r

    # 2. Mesma forma: quadros, resolução, fps, pixel e duração.
    io, iv = q.info(original), q.info(variante)
    forma = [("quadros", io.quadros, iv.quadros), ("largura", io.largura, iv.largura),
             ("altura", io.altura, iv.altura), ("fps", io.fps, iv.fps), ("pix_fmt", io.pix_fmt, iv.pix_fmt),
             ("duração do vídeo", round(io.duracao, 6), round(iv.duracao, 6))]
    diferencas = [f"{nome} {a} no original e {b} na variante" for nome, a, b in forma if a != b]
    r.append(Checagem(not diferencas, "mesma forma (quadros, resolução, fps, pixel e duração)"
                      if not diferencas else "forma diferente: " + "; ".join(diferencas)))
    if diferencas:
        return r

    # 3. O trecho que o certificado declara é o que a mudança diz.
    quadro_fim = q.quadros_antes_de(io, TRECHO_FIM)
    n_marca = q.primeiro_quadro_em(io, float(cert["marca_em"]))
    problemas = []
    if float(trecho["inicio"]) != TRECHO_INICIO or int(trecho["quadro_inicio"]) != 0:
        problemas.append(f"o trecho começa em {trecho['inicio']} s, e não no segundo 0")
    if float(trecho["fim"]) != TRECHO_FIM or int(trecho["quadro_fim"]) != quadro_fim:
        problemas.append(f"o trecho declarado termina no quadro {trecho['quadro_fim']}, e o 1º segundo "
                         f"termina no {quadro_fim}")
    if n_marca_cert != n_marca:
        problemas.append(f"o quadro da marca declarado é o {n_marca_cert}, e o de {cert['marca_em']} s é o {n_marca}")
    if set(fora_cert) != set(range(quadro_fim, io.quadros)):
        problemas.append("a lista de quadros fora do trecho não cobre exatamente os quadros depois do trecho")
    r.append(Checagem(not problemas, "o trecho declarado é [0, 1 s) e o quadro da marca é o do segundo da marca"
                      if not problemas else "; ".join(problemas)))
    if problemas:
        return r

    # 4 e 5. Quadro a quadro, decodificando os dois.
    hashes_original: list[str] = []
    hashes_variante: list[str] = []
    for a, b in zip(q.ler(original, io), q.ler(variante, iv)):
        hashes_original.append(q.sha256(a))
        hashes_variante.append(q.sha256(b))
    if len(hashes_original) != io.quadros or len(hashes_variante) != iv.quadros:
        r.append(Checagem(False, f"o decodificador deu {len(hashes_original)} e {len(hashes_variante)} quadros, "
                                 f"e o ffprobe {io.quadros}"))
        return r

    fora = range(quadro_fim, io.quadros)
    difere = [n for n in fora if hashes_variante[n] != hashes_original[n]]
    fora_do_cert = [n for n in fora if fora_cert[n] != hashes_original[n]]
    if difere:
        r.append(Checagem(False, f"mudança fora do trecho: o quadro {difere[0]} da variante difere do original "
                                 f"({len(difere)} de {len(fora)} quadros fora diferem: {_amostra(difere)})"))
    else:
        r.append(Checagem(True, f"fora do trecho, os {len(fora)} quadros da variante são iguais aos do original"))
    if fora_do_cert:
        r.append(Checagem(False, f"o hash do certificado não bate com o original no quadro {fora_do_cert[0]} "
                                 f"({len(fora_do_cert)} quadros)"))

    marca = hashes_original[n_marca]
    if marca != cert["quadro_da_marca"]["hash"]:
        r.append(Checagem(False, f"o hash do quadro da marca ({n_marca}) no certificado não é o do original"))
    trecho_ns = range(0, quadro_fim)
    nao_e_marca = [n for n in trecho_ns if hashes_variante[n] != marca]
    mudou = [n for n in trecho_ns if hashes_variante[n] != hashes_original[n]]
    if not mudou:
        r.append(Checagem(False, "cópia: nada mudou no trecho que o certificado declara (os quadros "
                                 f"0 a {quadro_fim - 1} da variante são os do original)"))
    elif nao_e_marca:
        r.append(Checagem(False, f"no trecho, o quadro {nao_e_marca[0]} da variante não é o quadro da marca "
                                 f"({len(nao_e_marca)} de {len(trecho_ns)}: {_amostra(nao_e_marca)})"))
    else:
        r.append(Checagem(True, f"no trecho, os {len(trecho_ns)} quadros são o quadro {n_marca} do original "
                                f"(a marca), e {len(mudou)} deles diferem do original"))

    # 6. Uma mudança só: o áudio não mexe.
    audio_o, audio_v = q.hash_do_audio(original), q.hash_do_audio(variante)
    if audio_o == audio_v:
        r.append(Checagem(True, "o áudio decodificado é igual ao do original" if audio_o else "nenhum dos dois tem áudio"))
    else:
        r.append(Checagem(False, "o áudio da variante difere do original"))

    # 7. O arquivo é o que o certificado registrou.
    sha_variante = q.sha256_do_arquivo(variante)
    r.append(Checagem(sha_variante == cert["variante"]["sha256"],
                      f"a variante tem o sha256 do certificado ({sha_variante[:12]})"))
    return r
