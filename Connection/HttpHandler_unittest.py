import unittest
from http.server import HTTPServer
from Connection.HttpHandler import WebHandlerHttp
import json
from threading import Thread
import requests
import filecmp
from Database.Utils import FileIO


class WebServetHttpTest(unittest.TestCase):
    def setUp(self):
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, WebHandlerHttp)
        thread = Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.user = json.loads(open("Database/Data/new user.json").read())
        self.name = (next(iter(self.user.keys())))
        self.password = self.user[self.name]["PASSWORD"]
        self.email = self.user[self.name]["email"]
        return

    def test_get(self):
        headers = {"Authorization": self.name + ":" + self.password}
        r = requests.get("http://localhost:8000/download", headers=headers)
        print(r.json())
        expected = json.loads(open("Database/Data/" + self.name + ".json").read())
        self.assertEqual(r.json(), expected, "Send message does not equal received message")

    def test_post(self):    #todo update
        headers = {"Authorization": self.name + ":" + self.password}
        with open("SampleImages/test.jpg", 'rb') as data:
            requests.post("http://localhost:8000/add", data=data, headers=headers)
        self.assertEqual(filecmp.cmp("SampleImages/test.jpg", "test.jpg"), True, "Send message does not equal received message")

    def run_all(self):
        self.setUp()
        self.test_get()
        self.test_post()



