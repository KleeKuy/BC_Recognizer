from http.server import BaseHTTPRequestHandler
from Connection.InputHandler import InputHandler
import json


class WebHandlerHttp(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        handlers = InputHandler().get_handlers()
        res = handlers[self.path](self.headers)
        if res is None:
            self.send_response(234)
            return
        data = json.dumps(res).encode('utf-8')
        self.send_response(200)
        self.send_header('content-type', ".json")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        print(self.path)
        handlers = InputHandler().get_handlers()
        content_len = int(self.headers.get('Content-Length'))
        print(content_len)
        if content_len == 0:
            body = None
        else:
            body = self.rfile.read(content_len)
        print("will now handle")
        res = handlers[self.path](body, self.headers)
        print("done handling")
        self.send_response(res)
        self.end_headers()


