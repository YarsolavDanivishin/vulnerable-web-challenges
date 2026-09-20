import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/flag":
            self.send_error(404)
            return
        body = os.environ.get("FLAG", "vladilk{local-ssrf-redirect}").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        return


HTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
