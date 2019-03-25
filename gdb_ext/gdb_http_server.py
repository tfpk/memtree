import json
import os

from http.server import HTTPServer, BaseHTTPRequestHandler

PATH_TO_CLIENT = "../client"


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/dump"):
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            dump_text = json.dumps(HTTPRequestHandler.CURRENT_DUMP)
            bytes_text = bytes(dump_text, encoding='utf-8')
            self.wfile.write(bytes_text)
            return

        if '..' in self.path:
            self.send_error(403, f'File Not Found: {self.path}')
            return

        self.send_response(200)
        if len(self.path) < 2:
            self.path = '/index.html'

        filetype = self.path.split('.')[-1]
        if filetype in ['js']:
            filetype = 'text'

        self.send_header('Content-type', f'text/{filetype}')
        self.end_headers()
        file_path = os.path.dirname(os.path.abspath(__file__))
        serve_path = os.path.join(file_path, PATH_TO_CLIENT, self.path[1:])
        with open(serve_path, 'rb') as serve_file:
            self.wfile.write(serve_file.read())


def run(dump):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    HTTPRequestHandler.CURRENT_DUMP = dump
    try:
        print("Starting Server...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping Serving...")
