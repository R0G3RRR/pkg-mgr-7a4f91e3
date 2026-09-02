import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = r"C:\Users\roger.santos\Downloads\redecanais-updates"

class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/log':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
            
            log_filepath = os.path.join(DIRECTORY, "tv_full_debug.log")
            with open(log_filepath, "w", encoding="utf-8") as f:
                f.write(post_data)
            
            print(f"[LOG SERVER] Received TV Full Diagnostic Log ({len(post_data)} bytes) -> Saved to tv_full_debug.log")
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_error(404, "Not Found")

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), LoggingHTTPRequestHandler) as httpd:
        print(f"[SERVER] High-Speed Local Server & Log Collector active at http://0.0.0.0:{PORT}/")
        httpd.serve_forever()
