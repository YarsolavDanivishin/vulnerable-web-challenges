import html
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

FLAG_PATH = Path("/opt/secret/flag.txt")
FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
FLAG_PATH.write_text(os.environ.get("FLAG", "vladilk{local-ssrf-nginx-waf}"), encoding="utf-8")


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        target = parse_qs(urlparse(self.path).query).get("url", [""])[0]
        result = ""
        if target:
            try:
                # The WAF only sees the original request. This fetcher performs
                # no equivalent destination validation.
                with urlopen(target, timeout=3) as response:
                    result = response.read(8192).decode("utf-8", errors="replace")
            except Exception as exc:
                result = f"Error: {exc}"
        body = f"""<!doctype html>
<title>Nginx WAF SSRF</title>
<h1>Nginx WAF SSRF</h1>
<p>The edge proxy blocks obvious loopback spellings.</p>
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


class InternalHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/admin/flag":
            self.send_error(404)
            return
        body = os.environ.get("FLAG", "vladilk{local-ssrf-nginx-waf}").encode()
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
HTTPServer(("0.0.0.0", 8080), AppHandler).serve_forever()
