import unittest
from threading import Thread
from Connection.WebHandler import WebHandler
import socket
import base64


class WebServetTest(unittest.TestCase):
    def test(self):

        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005

        handler = {'TST': lambda dta: self.test_handle(dta)}

        web = WebHandler(ip=TCP_IP, port=TCP_PORT, handlers=handler)
        thread = Thread(target=web.listen)
        thread.start()

        BUFFER_SIZE = 1024
        cmd = "TST"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))

        cmdenc = cmd.encode('utf-8')
        with open("SampleImages/w4.jpg", 'rb') as img:
            image = base64.b64encode(img.read())
        s.send(cmdenc)
        s.send(image)
        rec = s.recv(BUFFER_SIZE)
        #msg = data.decode('utf-8')
        s.close()

    def test_handle(self,
                    data):
        with open("SampleImages/new_image.jpg", 'wb') as f:
            enc = base64.b64decode(data)
            f.write(enc)
        print("test handle")
        return "response"


