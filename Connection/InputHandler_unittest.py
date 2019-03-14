from Connection.InputHandler import InputHandler
from Database.UsersDatabase import UsersDatabase
from Database.DataBase import DataBase
import unittest
import os
import json


class InputTest(unittest.TestCase):
    def setUp(self):
        self.handler = InputHandler(db="test")
        self.user = json.loads(open("Database/Data/new user.json").read())
        self.name = (next(iter(self.user.keys())))
        self.password = self.user[self.name]["PASSWORD"]
        self.email = self.user[self.name]["email"]

    def test_add_user(self):
        try:
            os.remove("Database/Data/test.json")
        except FileNotFoundError:
            print("file already removed")
        creds = {"name": self.name,
                 "password": self.password,
                 "email": self.email}
        res = self.handler.add_user(str(creds).encode('utf-8'))
        self.assertEqual(res, 200, "1 Input add user test failed, wrong reposnse!")
        db = UsersDatabase(name="test")
        self.assertEqual(db.verify_user(self.password, self.name), True, "2 Input add user test failed!")
        res = self.handler.add_user(str(creds).encode('utf-8'))
        self.assertEqual(res, 234, "3 Input add user test failed, wrong reposnse!")

    def test_verify(self):
        # test_add_user
        headers = {"Authorization": self.name + ":" + self.password}
        headers_wrong = {"Authorization": "asdawd:adwadadfa"}
        res = self.handler.verify_user(headers)
        self.assertEqual(res, 200, "1 Input verify test failed")
        res = self.handler.verify_user(headers_wrong)
        self.assertEqual(res, 234, "2 Input verify test failed")

    def test_send_databse(self):
        # test_add_user
        self.populate_db()
        headers = {"Authorization": self.name + ":" + self.password}
        ret = self.handler.send_databse(headers)
        print(ret)
        print("Database/Data/" + self.name + ".json")
        expected = json.loads(open("Database/Data/" + self.name + ".json").read())
        self.assertEqual(expected, ret, "Input get test failed")

    def test_rec_img(self):
        pass  # todo

    def test_decode_json(self):
        pass  # todo

    def populate_db(self):
        db = DataBase(name=self.name)
        db.add_record(json.loads(open("Database/Data/BC1.json").read()))
        db.add_record(json.loads(open("Database/Data/BC2.json").read()))

    def run_all(self):
        self.setUp()
        self.test_add_user()
        self.test_verify()
        self.test_send_databse()
