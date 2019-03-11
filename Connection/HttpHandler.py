from http.server import BaseHTTPRequestHandler
from socketserver import BaseRequestHandler
from Connection.InputHandler import InputHandler
import ast
import json
from time import sleep


class WebHandlerHttp(BaseHTTPRequestHandler):

    def do_GET(self):   #TODO
        # self.wfile.write(handlers[self.path()])
        if self.path == "/download":
            handlers = InputHandler().get_handlers()
            res = handlers[self.path](self.headers)
            if res is None:
                self.send_response(404)
                return
            data = json.dumps(res).encode('utf-8')
            self.send_response(200)
            self.send_header('content-type', ".json")
            self.end_headers()
            self.wfile.write(data)


        print(self.path)
        if self.path == "/user":
            self.send_response(200)
            self.send_header('content-type', ".json")
            self.end_headers()
            with open("Database/Data/test.json") as user:
                msg = user.read()
                data = msg.encode('utf-8')  #TODO send actual user data (name, email)
                print("sending " + msg)
                self.wfile.write(data)      #TODO Needed new method in db that will return user data without password
        if self.path == "/data":
            print("send database")

    def do_POST(self):
        if self.path == "/add":
            handlers = InputHandler().get_handlers()
            content_len = int(self.headers.get('Content-Length'))
            print(content_len)
            if content_len == 0:
                body = None
            else:
                body = self.rfile.read(content_len)
            res = handlers[self.path](body, self.headers)
            self.send_response(res)
            self.end_headers()
            return

        print(self.path)
        handlers = InputHandler().get_handlers()
        content_len = int(self.headers.get('Content-Length'))
        print(content_len)
        if content_len == 0:
            body = None
        else:
            body = self.rfile.read(content_len).decode('utf-8')
            body = ast.literal_eval(body)
        res = handlers[self.path](body, self.headers)
        self.send_response(res)
        self.end_headers()


#        print("posted to path " + self.path)
#        if self.path == "/verify":
#            print("to verify")
#            print("headers " + str(self.headers))
#            self.send_response(200)
#            self.end_headers()
#            print("done posting")
#        elif self.path == "/register":
#            print(self.headers.get('content-type'))
#            post_body = self.rfile.read(content_len)
#            print("post body is " + post_body.decode('utf-8'))
#            #register