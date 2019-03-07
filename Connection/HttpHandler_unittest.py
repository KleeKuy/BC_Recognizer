import unittest
from http.server import HTTPServer
from Connection.HttpHandler import WebHandlerHttp
from time import sleep
from threading import Thread
import requests
from Database.Utils import FileIO


class WebServetHttpTest(unittest.TestCase):
    def test(self):
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, WebHandlerHttp)
        thread = Thread(target=httpd.serve_forever)
        thread.start()
        sleep(1)

        #self.test_get()
        #self.test_post()

        sleep(5)
        return

    def test_get(self):
        print("get testing")
        r = requests.get("http://10.1.2.104:8000/user")
       # print(r.status_code)
       # print(r.reason)
       # print(r.headers['content-type'])
        FileIO.write_json(file="Database/Data/testhttp.json", data=r.json())
        inp = FileIO.read_json("Database/Data/testhttp.json")
        test = FileIO.read_json("Database/Data/test.json")
        self.assertEqual(inp, test, "Send message does not equal received message")

    def test_post(self):
        print("post testing")
        test = FileIO.read_json("Database/Data/test.json")
        headers = {'content-type': "application/json"}
        r = requests.post("http://10.1.2.104:8000/verify", data=str(test), headers=headers)
        print(r.status_code)
      #  print(r.reason)
      #  print(r.headers['content-type'])
      #  print(r.encoding)
      #  print(r.text)
      #  print(r.json())


