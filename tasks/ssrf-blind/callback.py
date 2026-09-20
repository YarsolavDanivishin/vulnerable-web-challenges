import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

RESULTS = Path("/shared")
RESULTS.mkdir(exist_ok=True)
Path("/opt/secret").mkdir(parents=True, exist_ok=True)
Path("/opt/secret/flag.txt").write_text(os.environ.get("FLAG", "vladilk{local-blind-ssrf}"), encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        query = parse_qs(urlparse(self.path).query)
        command = query.get("cmd", ["printf callback-ok"])[0]
        token = query.get("token", ["callback"])[0]
        # Deliberately vulnerable training sink, isolated inside this container.
        completed = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=3)
        output = completed.stdout + completed.stderr
        (RESULTS / token).write_text(output[:8192], encoding="utf-8")
        body = b"accepted"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        return


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
