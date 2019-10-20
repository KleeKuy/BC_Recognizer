import unittest
from Database.DataBase import DataBase
from Database.Utils import Mode
import json
import os
import copy
from threading import Thread


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        try:
            os.remove("Database/Data/database.db")
        except FileNotFoundError:
            print("file already removed!")
        self.db = DataBase()
        self.user1 = {
            "name": "Rick Sanchez",
            "password": "Wubba Lubba Dub-Dub",
            "email": "rick@mail.com"
        }
        self.user2 = {
            "name": "Talos Valcoran",
            "password": "Dasovallia",
            "email": "talos@echo.com"
        }
        self.user3 = {
            "name": "Uzas",
            "password": "BFDBG",
            "email": "uzas@khorne.com"
        }

        self.add_user = lambda user: self.db.add_user(user["name"], user["password"], user["email"])

        self.recname1 = "Indrick Boreale"
        self.recname2 = "Vandred Anrathi"
        self.recname3 = "Cyrion"
        self.rec1 = {self.recname1: {"email": "indrick@Kaurava.ultima", "telefon": "13432425253",
                                     "website": "www.cptBoreale.dr"}}
        self.rec2 = {self.recname2: {"alias": "The Exalted", "email": "exalted@Covenant.com",
                                     "adres": "The Covenant"}}
        self.rec3 = {self.recname3: {"fax": "123221", "affiliation": "slaanesh",
                                     "email": "Cyrion@firstclaw.covenant"}}

    def test_verify(self):
        self.add_user(self.user1)
        self.assertEqual(True, self.db.verify_user(self.user1["name"], self.user1["password"]),
                         "1 Verify true test failed!")
        self.add_user(self.user1)
        self.assertEqual(False, self.db.verify_user(self.user1["name"], self.user2["password"]),
                         "2 Verify false test failed!")
        self.add_user(user=self.user1)
        self.assertEqual(False, self.db.verify_user(self.user2["name"], self.user1["password"]),
                         "3 Verify false test failed!")

    def test_add_user(self):
        self.db.remove_user(self.user1["name"])
        self.add_user(self.user2)
        self.assertEqual(True, self.db.verify_user(self.user2["name"], self.user2["password"]),
                         "1 Add to empty db test failed!")
        self.add_user(self.user1)
        self.db.add_user(self.user2["name"], self.user1["password"], self.user1["email"])
        self.db.add_user(self.user1["name"], self.user1["password"], self.user1["email"])
        self.assertEqual(True, self.db.verify_user(self.user1["name"], self.user1["password"]),
                         "2 Add to non empty db test failed!")
        self.assertEqual(True, self.db.verify_user(self.user2["name"], self.user2["password"]),
                         "3 Add override db test failed!")
        self.db.remove_user(self.user2["name"])
        ret = self.add_user(self.user2)
        self.assertEqual(True, ret, "4 Add incorect return value!")
        ret = self.add_user(self.user2)
        self.assertEqual(False, ret, "5 Add incorect return value!")

    def test_remove_user(self):
        self.db.remove_user(self.user1["name"])
        self.db.remove_user(self.user2["name"])
        self.assertEqual(False, self.db.verify_user(self.user1["name"], self.user1["password"]),
                         "1 Remove not existing record test failed!")
        self.add_user(self.user2)
        self.db.remove_user(self.user2["name"])
        self.assertEqual(False, self.db.verify_user(self.user1["name"], self.user1["password"]),
                         "2 Remove only record test failed!")
        self.add_user(self.user1)
        self.add_user(self.user2)
        self.db.remove_user(self.user1["name"])
        self.assertEqual(False, self.db.verify_user(self.user1["name"], self.user1["password"]),
                         "3.1 Remove one record test failed! - record not removed")
        self.assertEqual(True, self.db.verify_user(self.user2["name"], self.user2["password"]),
                         "3.2 Remove one record test failed! - other record corrupted!")
        self.db.remove_user(self.user1["name"])
        self.db.remove_user(self.user1["name"])
        self.db.remove_user(self.user1["name"])
        self.assertEqual(False, self.db.verify_user(self.user1["name"], self.user1["password"]),
                         "4.1 Remove not existing record test failed! - record not removed")
        self.assertEqual(True, self.db.verify_user(self.user2["name"], self.user2["password"]),
                         "4.2 Remove not existing record test failed! - other record corrupted!")

    def test_update_user(self):
        # assusre that user1 is self.user1
        self.db.remove_user(self.user1["name"])
        self.add_user(self.user1)

        new_pass = "asdadsa"
        self.db.update_user(self.user1["name"], new_pass)

        self.assertEqual(False, self.db.verify_user(self.user1["name"], self.user1["password"]),
                         "1 Update user updated failed! - record not changed")
        self.assertEqual(True, self.db.verify_user(self.user1["name"], new_pass),
                         "2 Updated user test failed!")

    def test_add_record(self):
        # assusre that user1 is self.user1
        self.db.remove_user(self.user1["name"])
        self.add_user(self.user1)

        self.db.add_record(self.user1["name"], self.rec1)
        res = self.db.view_database(self.user1["name"])
        self.assertEqual(res, self.rec1, "1 Add record Failed - first record, first user ")

        self.db.remove_user(self.user2["name"])
        self.add_user(self.user2)

        self.db.add_record(self.user2["name"], self.rec1)
        res = self.db.view_database(self.user2["name"])
        self.assertEqual(res, self.rec1, "2 Add record Failed - first record, second user ")

        self.db.add_record(self.user1["name"], self.rec2)
        res = self.db.view_database(self.user1["name"])
        rec = copy.deepcopy(self.rec1)
        rec.update(self.rec2)
        self.assertEqual(res, rec, "3 Add record Failed - second record, first user ")

        self.db.add_record(self.user1["name"], self.rec3)
        res = self.db.view_database(self.user1["name"])
        rec.update(self.rec3)
        self.assertEqual(res, rec, "4 Add record Failed - third record, first user ")

        # TODO duplicate names

    def test_remove_record(self):
        self.db.remove_user(self.user1["name"])
        self.db.remove_user(self.user2["name"])
        self.add_user(self.user1)

        self.db.add_record(self.user1["name"], self.rec1)
        self.db.remove_record(self.user1["name"], self.recname1)
        self.assertEqual({}, self.db.view_database(self.user1["name"]),
                         "1 Remove record - only one record ")

        self.db.add_record(self.user1["name"], self.rec1)
        self.db.add_record(self.user1["name"], self.rec2)
        self.db.remove_record()


    def test_thread_safety(self):
        thread = Thread(target=self.async_fun)
        thread2 = Thread(target=self.async_fun)
        thread3 = Thread(target=self.async_fun)
        thread.start()
        thread2.start()
        thread3.start()

        thread.join()
        thread2.join()
        thread3.join()
        self.remove_user("Wonsz")
        self.add_user(self.new_user)
        self.assertEqual(True, self.verify_user("Wonsz", "rzeczny"), "Thread test failed!")

    def async_fun(self):
        i = 0
        while i < 15:
            i += 1
            self.add_user(user=self.new_user)
            self.update_user(user=self.updated)
            self.remove_user("Wonsz")
            self.add_user(user=self.new_user2)
            self.verify_user("Wonsz", "rzeczny")
            self.remove_user("Wonsz2")

    def run_all(self):
        self.setUp()
        self.test_verify()
        self.test_add_user()
        self.test_remove_user()
        self.test_update_user()
        self.test_add_record()
        self.test_remove_record()
   #     self.test_thread_safety()


if __name__ == '__main__':
    unittest.main()
