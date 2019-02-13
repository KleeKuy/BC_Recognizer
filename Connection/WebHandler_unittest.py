import unittest
from threading import Thread
from Connection.WebHandler import WebHandler
import socket
import base64
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

    def start_test(self):
        thread = Thread(target=self.web.listen)
        thread.start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, self.TCP_PORT))
        return s

    def test_img(self):
        s = self.start_test()
        cmdenc = 'IMG'.encode('utf-8')
        with open("SampleImages/w4.jpg", 'rb') as img:
            image = base64.b64encode(img.read())
        s.send(cmdenc)
        s.send(image)
        rec = s.recv(BUFFER_SIZE)
        msg = rec.decode('utf-8')
        self.assertEqual(msg, "text retrieved from image", "Image send test failed")
        s.send('END'.encode('utf-8'))
        s.close()

    def test_str(self):
        s = self.start_test()
        cmdenc = 'STR'.encode('utf-8')
        data = "Test message!"
        s.send(cmdenc)
        s.send(data.encode('utf-8'))
        rec = s.recv(BUFFER_SIZE)
        msg = rec.decode('utf-8')
        self.assertEqual(msg, "Test message!", "Text send test failed")
        s.send('END'.encode('utf-8'))
        s.close()

    def img_handle(self,
                   data):
        with open("SampleImages/new_image.jpg", 'wb') as f:
            enc = base64.b64decode(data)
            f.write(enc)
        return "text retrieved from image"

    def str_handle(self,
                   data):
        return data.encode('utf-8')

    def run_all(self):
        self.setUp()
        self.test_img()
