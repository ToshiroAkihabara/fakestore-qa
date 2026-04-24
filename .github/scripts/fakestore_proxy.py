from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests


TARGET = 'https://fakestoreapi.com'


class Handler(BaseHTTPRequestHandler):
    def _send_response(self, response):
        self.send_response(response.status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')

        content_type = response.headers.get('Content-Type', 'application/json')
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(response.content)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.end_headers()

    def do_GET(self):
        try:
            response = requests.get(f'{TARGET}{self.path}', timeout=15)
        except requests.RequestException as error:
            self.send_json_error(502, str(error))
            return

        self._send_response(response)

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        try:
            response = requests.post(
                f'{TARGET}{self.path}',
                data=body,
                headers={
                    'Content-Type': self.headers.get(
                        'Content-Type',
                        'application/json',
                    ),
                },
                timeout=15,
            )
        except requests.RequestException as error:
            self.send_json_error(502, str(error))
            return

        self._send_response(response)

    def send_json_error(self, status, message):
        body = f'{{"error": {message!r}}}'.encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


print('Fake Store proxy listening on http://127.0.0.1:8000', flush=True)
ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
