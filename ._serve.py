import http.server, os, socketserver

ROOT = r"E:\tavern characters"

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()
    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()
    def log_message(self, fmt, *args):
        print(self.address_string(), "-", fmt % args, flush=True)

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with TS(("0.0.0.0", 8899), CORSHandler) as httpd:
        print("Serving on 0.0.0.0:8899 with CORS *", flush=True)
        httpd.serve_forever()
