import hashlib
import html
import os
import secrets
import socket
import struct
import threading
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

FLAG_PATH = Path("/opt/secret/flag.txt")


def generate_flag() -> str:
    configured = os.environ.get("FLAG")
    if configured:
        return configured
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()


FLAG = generate_flag()
FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
FLAG_PATH.write_text(FLAG, encoding="utf-8")


def resolve_once(host: str) -> str:
    transaction_id = os.urandom(2)
    labels = (
        b"".join(bytes([len(label)]) + label.encode() for label in host.split("."))
        + b"\0"
    )
    packet = (
        transaction_id
        + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        + labels
        + struct.pack("!HH", 1, 1)
    )
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns:
        dns.settimeout(2)
        dns.sendto(packet, (os.environ.get("DNS_SERVER", "dns"), 5353))
        response = dns.recv(512)
    if response[:2] != transaction_id or len(response) < 4 or response[3] == 0:
        raise ValueError("DNS resolution failed")
    return socket.inet_ntoa(response[-4:])


def fetch(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme != "http" or not parsed.hostname:
        raise ValueError("use an http URL")

    # The validator resolves once and accepts the apparently public address.
    safe_ip = resolve_once(parsed.hostname)
    if safe_ip in {"127.0.0.1", "0.0.0.0", "::1"}:
        raise ValueError("loopback address blocked")

    # The vulnerable client resolves again when connecting.
    destination = resolve_once(parsed.hostname)
    connection = HTTPConnection(destination, parsed.port or 80, timeout=3)
    connection.request("GET", parsed.path or "/", headers={"Host": parsed.hostname})
    response = connection.getresponse()
    return response.read(8192).decode("utf-8", errors="replace")


class PublicHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        target = parse_qs(urlparse(self.path).query).get("url", [""])[0]
        try:
            result = fetch(target) if target else ""
        except Exception as exc:
            result = f"Error: {exc}"
        body = f"<h1>DNS Rebinding SSRF</h1><p>Validation and connection use separate DNS lookups.</p><form><input name='url' value='{html.escape(target)}' size='70'><button>Fetch</button></form><pre>{html.escape(result)}</pre>".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        return


class InternalHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/admin/flag":
            self.send_error(404)
            return
        body = FLAG.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        return


threading.Thread(
    target=lambda: HTTPServer(("127.0.0.1", 8081), InternalHandler).serve_forever(),
    daemon=True,
).start()
HTTPServer(("0.0.0.0", 80), PublicHandler).serve_forever()
