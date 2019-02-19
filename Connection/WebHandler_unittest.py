import unittest
from threading import Thread
import socket
import base64
from Connection.WebHandler import WebHandler
BUFFER_SIZE = 1024


class WebServetTest(unittest.TestCase):
    def setUp(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 50000
        self.handlers = {
            'IMG': lambda data: self.img_handle(data),
            'STR': lambda data: self.str_handle(data)
        }
        self.web = WebHandler(handlers=self.handlers)
        self.res = None
        t = Thread(target=self.web.run, daemon=True)
        t.start()

    def send(self,
             data,
             cmd):
        port = self.TCP_PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, port))
        s.send(cmd)
        s.send(data)
        rec = s.recv(BUFFER_SIZE)
        msg = rec.decode('utf-8')
        s.send('END'.encode('utf-8'))
        s.close()
        self.res = msg

    def test_img(self):
        cmdenc = 'IMG'.encode('utf-8')
        with open("SampleImages/w4.jpg", 'rb') as img:
            image = base64.b64encode(img.read())
            thread = Thread(target=self.send, args=(image, cmdenc))
            thread.start()
        thread.join()
        self.assertEqual(self.res, "text retrieved from image", "Image send test failed")

    def test_str(self,
                 data="Test message!"):
        cmdenc = 'STR'.encode('utf-8')
        self.send(data.encode('utf-8'), cmdenc)
        self.assertEqual(self.res, data, "Image send test failed")

    def test_many_connections(self):
        i = 0
        while i < 10:
            t1 = Thread(target=self.test_str, args=str(i))
            t2 = Thread(target=self.test_img)
            t1.start()
            t2.start()
            i += 1

    def img_handle(self,
                   data):
        with open("SampleImages/new_image.jpg", 'wb') as f:
            enc = base64.b64decode(data)
            f.write(enc)
        return "text retrieved from image"

    def str_handle(self,
                   data):
        return data.decode('utf-8')

    def run_all(self):
        self.setUp()
        self.test_img()
        self.test_str() #TODO sometimes it can happen that we have delay after command and data is new command
        self.test_many_connections()
