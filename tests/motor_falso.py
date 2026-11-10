"""Um motor falso, local, que cumpre contrato/motor.md, para provar que o teste de contrato pega cada falha.

    MOTOR_KEY=<teste> MOTOR_SECRET=<teste> python tests/motor_falso.py [--porta 8765] [--limite-mb 100]
        [--adulterar sem_request_id|200_sem_token|401_com_token]

As credenciais que ele aceita vêm do ambiente (valores de teste, nunca os do motor real).
Ele não lê o vídeo: devolve contrato/exemplos/resposta-ok.json com um request_id novo e o
sha256 do arquivo recebido. Na primeira linha da saída, imprime a URL em que escuta.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from email.parser import BytesParser
from email.policy import HTTP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RESPOSTA_OK = RAIZ / "contrato" / "exemplos" / "resposta-ok.json"
ADULTERACOES = ("sem_request_id", "200_sem_token", "401_com_token")


def _partes(content_type: str, corpo: bytes) -> dict[str, tuple[str | None, bytes]]:
    msg = BytesParser(policy=HTTP).parsebytes(b"Content-Type: " + content_type.encode("latin-1") + b"\r\n\r\n" + corpo)
    if not msg.is_multipart():
        return {}
    partes = {}
    for parte in msg.iter_parts():
        nome = parte.get_param("name", header="content-disposition")
        if nome:
            partes[nome] = (parte.get_filename(), parte.get_payload(decode=True) or b"")
    return partes


def servidor(porta: int, chave: str, segredo: str, limite_mb: float, adulterar: str | None) -> ThreadingHTTPServer:
    modelo = json.loads(RESPOSTA_OK.read_text(encoding="utf-8"))
    limite = int(limite_mb * 1024 * 1024)

    class Motor(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args) -> None:  # silencioso: o pytest mostra o que importa
            pass

        def _json(self, codigo: int, corpo: dict) -> None:
            dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(dados)))
            self.end_headers()
            self.wfile.write(dados)

        def _autorizado(self) -> bool:
            if adulterar == "401_com_token":
                return False
            if adulterar == "200_sem_token":
                return True
            return self.headers.get("Modal-Key") == chave and self.headers.get("Modal-Secret") == segredo

        def _ler_corpo(self) -> bytes:
            tamanho = int(self.headers.get("Content-Length") or 0)
            return self.rfile.read(tamanho)

        def do_GET(self) -> None:
            if not self._autorizado():
                self._json(401, {"erro": "nao_autorizado", "mensagem": "missing credentials for proxy authorization"})
            elif self.path == "/saude":
                self._json(200, {"ok": True, "versao_contrato": modelo["versao_contrato"]})
            else:
                self._json(404, {"erro": "rota_desconhecida", "mensagem": self.path})

        def do_POST(self) -> None:
            corpo = self._ler_corpo()
            if not self._autorizado():
                return self._json(401, {"erro": "nao_autorizado", "mensagem": "missing credentials for proxy authorization"})
            if self.path != "/analisar":
                return self._json(404, {"erro": "rota_desconhecida", "mensagem": self.path})
            if len(corpo) > limite:
                return self._json(413, {"erro": "video_grande_demais", "mensagem": f"o limite é {limite_mb:g} MB"})
            partes = _partes(self.headers.get("Content-Type", ""), corpo)
            if "video" not in partes or "marca" not in partes:
                return self._json(422, {"erro": "pedido_invalido", "mensagem": "faltam os campos video e marca"})
            marca = partes["marca"][1].decode("utf-8", "replace").strip()
            if not 1 <= len(marca) <= 60:
                return self._json(422, {"erro": "pedido_invalido", "mensagem": "a marca tem de ter de 1 a 60 caracteres"})
            video = partes["video"][1]
            if video[4:8] != b"ftyp":
                return self._json(415, {"erro": "tipo_nao_suportado", "mensagem": "o vídeo tem de ser mp4 ou mov"})
            resposta = json.loads(json.dumps(modelo))
            resposta["request_id"] = uuid.uuid4().hex
            resposta["video_sha256"] = hashlib.sha256(video).hexdigest()
            if adulterar == "sem_request_id":
                del resposta["request_id"]
            self._json(200, resposta)

    return ThreadingHTTPServer(("127.0.0.1", porta), Motor)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python tests/motor_falso.py", description=__doc__.split("\n")[0])
    p.add_argument("--porta", type=int, default=8765, help="0 escolhe uma porta livre")
    p.add_argument("--limite-mb", type=float, default=100.0)
    p.add_argument("--adulterar", choices=ADULTERACOES)
    a = p.parse_args(argv)
    chave, segredo = os.environ.get("MOTOR_KEY"), os.environ.get("MOTOR_SECRET")
    if not chave or not segredo:
        print("erro: ponha MOTOR_KEY e MOTOR_SECRET (valores de teste) no ambiente", file=sys.stderr)
        return 2
    s = servidor(a.porta, chave, segredo, a.limite_mb, a.adulterar)
    print(f"motor falso em http://127.0.0.1:{s.server_address[1]}" + (f" (adulterado: {a.adulterar})" if a.adulterar else ""),
          flush=True)
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
