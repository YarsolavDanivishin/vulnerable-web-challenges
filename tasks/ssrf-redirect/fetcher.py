import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        target = parse_qs(urlparse(self.path).query).get("url", [""])[0]
        result = ""
        if target:
            try:
                # The bug is that the final URL is not validated after redirects.
                with urlopen(target, timeout=3) as response:
                    result = response.read(8192).decode("utf-8", errors="replace")
            except Exception as exc:
                result = f"Error: {exc}"

        body = f"""<!doctype html>
<title>SSRF Redirect</title>
<h1>SSRF Redirect</h1>
<p>The fetcher follows redirects automatically.</p>
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
