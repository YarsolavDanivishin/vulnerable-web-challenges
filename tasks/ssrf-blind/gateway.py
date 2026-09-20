import html
import secrets
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

RESULTS = Path("/shared")
RESULTS.mkdir(exist_ok=True)


def dispatch(url: str, token: str) -> None:
    try:
        with urlopen(url, timeout=5) as response:
            response.read(4096)
        status = "callback reached"
    except Exception as exc:
        status = f"request error: {exc}"
    (RESULTS / token).write_text(status, encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path == "/submit":
            target = query.get("url", [""])[0]
            token = secrets.token_hex(4)
            threading.Thread(target=dispatch, args=(target, token), daemon=True).start()
            body = f"Job accepted. Check /result?token={token} later."
        elif parsed.path == "/result":
            token = query.get("token", [""])[0]
            result = (
                (RESULTS / token).read_text(encoding="utf-8")
                if token and (RESULTS / token).is_file()
                else "pending"
            )
            body = f"<h1>Blind SSRF result</h1><pre>{html.escape(result)}</pre>"
        else:
            body = "<h1>Blind SSRF</h1><p>Submit a URL. The response body is never returned.</p>"
            body += "<form action='/submit'><input name='url' size='70'><button>Submit</button></form>"

        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args) -> None:
        return


HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
