import unittest
from threading import Thread
from Connection.WebHandler import WebHandler
import socket
import base64
from time import sleep
BUFFER_SIZE = 1024


class WebServetTest(unittest.TestCase):
    def setUp(self):

        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5005
        self.handlers = {
            'IMG': lambda data: self.img_handle(data),
            'STR': lambda data: self.str_handle(data)
        }
        self.web = WebHandler(ip=self.TCP_IP, port=self.TCP_PORT, handlers=self.handlers)
        self.res = None

    def send(self,
             data,
             cmd):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sleep(1)
        s.connect((self.TCP_IP, self.TCP_PORT))
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
        self.web.setup_connection()
        self.web.listen()
        thread.join()
        self.assertEqual(self.res, "text retrieved from image", "Image send test failed")

    def test_str(self):
        cmdenc = 'STR'.encode('utf-8')
        data = "Test message!"
        thread = Thread(target=self.send, args=(data.encode('utf-8'), cmdenc))
        thread.start()
        self.web.setup_connection()
        self.web.listen()
        thread.join()
        self.assertEqual(self.res, data, "Image send test failed")

    def img_handle(self,
                   data):
        with open("SampleImages/new_image.jpg", 'wb') as f:
            enc = base64.b64decode(data)
            f.write(enc)
        return "text retrieved from image"

    def str_handle(self,
                   data):
        return data

    def run_all(self):
        self.setUp()
        self.test_img()
        self.test_str()
