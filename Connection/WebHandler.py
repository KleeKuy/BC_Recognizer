from http.server import BaseHTTPRequestHandler


class WebHandler(BaseHTTPRequestHandler):

    def do_GET(self):   #TODO
        # print(self.path)
        if self.path == "/user":
            self.send_response(200)
            self.send_header('User verification', ".json")
            self.end_headers()
            with open("Database/Data/test.json") as user:
                msg = user.read()
                data = msg.encode('utf-8')  #TODO send actual user data (name, email)
                self.wfile.write(data)      #TODO Needed new method in db that will return user data without password
        if self.path == "/data":
            print("send database")
