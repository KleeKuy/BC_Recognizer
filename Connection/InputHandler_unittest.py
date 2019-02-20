from Connection.InputHandler import InputHandler
import unittest
import os
import json
EXAMPLE = "NAME:WONSZ2/PASSWORD:RZECZNY/EMAIL:JESTNIEBEZPIECZNY/DUDUDUDU:DUDUDUDU".encode('utf-8')
EXAMPLE2 = "NAME:WONSZ2/PASSWORD:RZECZNY".encode('utf-8')


class InputTest(unittest.TestCase):
    def setUp(self):
        self.handler = InputHandler(db="test")

    def test_add_user(self):
        try:
            os.remove("Database/Data/test.json")
        except FileNotFoundError:
            print("file already removed")
        self.handler.add_user(EXAMPLE)
        with open("Database/Data/test.json") as db:
            res = json.loads(db.read())
            expected = {"WONSZ2": {"PASSWORD": "RZECZNY", "EMAIL": "JESTNIEBEZPIECZNY", "DUDUDUDU": "DUDUDUDU"}}
            self.assertEqual(res, expected, "Input add user test failed!")

    def test_verify(self):
        self.handler.add_user(EXAMPLE)
        res = self.handler.verify_user(EXAMPLE2, "someip")
        self.assertEqual(res, "T", "Input verify test failed")

    def test_end(self):
        self.test_verify()
        self.handler.end_connection("someip")
        try:
            self.handler.db["someip"]
        except KeyError:
            return
        self.assertEqual(False, True, "Input end test failed")

    def run_all(self):
        self.setUp()
        self.test_add_user()
        self.test_verify()
        self.test_end()


