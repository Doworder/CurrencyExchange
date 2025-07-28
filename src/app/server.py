from http.server import BaseHTTPRequestHandler, HTTPServer


class CurrencyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"GET method called.")

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST method called.")

    def do_PATCH(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"PATCH method called.")

    def _add_currency[T](self, entity: T):
        db = SQLiteManager(Path("data/currency.db"))
        db.add_currency(entity)

    def _send_response(self, status_code: int, message=None):
        self.send_response(status_code, message)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

def main():
    server_address = ('', 8000)
    server = HTTPServer(server_address, CurrencyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == '__main__':
    main()