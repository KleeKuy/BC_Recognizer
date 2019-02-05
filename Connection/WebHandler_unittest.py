import unittest
from http.server import HTTPServer
from Connection.WebHandler import WebHandler
import urllib.request
from time import sleep
from threading import Thread


class WebServetTest(unittest.TestCase):
    def test(self):
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, WebHandler)
        thread = Thread(target=httpd.serve_forever)
        thread.start()

        sleep(1)
        print("send http request")
        contents = urllib.request.urlopen("http://localhost:8000/user").read()
        text = contents.decode('utf-8')
        # print("received messege: " + text)
        with open("Database/Data/test.json") as test:
            self.assertEqual(text, test.read(), "Send message does not equal received message")
        return
