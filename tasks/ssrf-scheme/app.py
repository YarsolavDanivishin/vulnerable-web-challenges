import html
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

FLAG_PATH = Path("/opt/secret/flag.txt")
FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
FLAG_PATH.write_text(os.environ.get("FLAG", "vladilk{local-ssrf-scheme}"), encoding="utf-8")


def fetch(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https", "file"}:
        with urlopen(url, timeout=3) as response:
            return response.read(8192).decode("utf-8", errors="replace")
    raise ValueError("unsupported URL scheme")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        query = parse_qs(urlparse(self.path).query)
        target = query.get("url", [""])[0]
        result = ""
        if target:
            try:
                result = fetch(target)
            except Exception as exc:
                result = f"Error: {exc}"

        body = f"""<!doctype html>
<title>SSRF Scheme</title>
<h1>SSRF Scheme</h1>
<p>Fetch a URL. The service accepts HTTP, HTTPS, and legacy file URLs.</p>
<form><input name="url" value="{html.escape(target)}" size="70"><button>Fetch</button></form>
<pre>{html.escape(result)}</pre>
""".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        return


HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
