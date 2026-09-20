import hashlib
import os
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer


def generate_flag() -> str:
    configured = os.environ.get("FLAG")
    if configured:
        return configured
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()


FLAG = generate_flag()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/flag":
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


HTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
