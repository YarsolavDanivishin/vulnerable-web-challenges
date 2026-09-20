from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        target = parse_qs(urlparse(self.path).query).get("to", [""])[0]
        self.send_response(302)
        self.send_header("Location", target or "http://internal:8081/flag")
        self.end_headers()

    def log_message(self, *_args) -> None:
        return


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
