import json
from urllib.parse import unquote
from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def _writeheaders(self):
        print(self.path)
        print(self.headers)

    def do_Head(self):
        self._writeheaders()

    def do_GET(self):
        # 返回响应
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Get request received".encode('utf-8'))

    def do_POST(self):
        self._writeheaders()
        data = self.rfile.read(int(self.headers['content-length']))
        data = unquote(str(data, encoding='utf-8'))
        try:
          json_obj = json.loads(data)
          print(json_obj)
        except:
          print(data)
        
        # 返回响应
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("POST request received".encode('utf-8'))


if __name__ == "__main__":
    addr = ('0.0.0.0', 8000)
    server = HTTPServer(addr, RequestHandler)
    server.serve_forever()
