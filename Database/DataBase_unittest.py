import unittest
from Database.DataBase import DataBase
from Database.Utils import Mode
import json
import os
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
            "password": "WDasovallia",
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
        self.rec3 = {self.recname2: {"fax": "123221", "affiliation": "slaanesh",
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

    def test_add(self):
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

    def test_remove(self):
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

    def test_update(self):
        self.assert_no_db()
        res1 = self.update_user(user=self.updated)
        self.assertEqual(False, self.verify_user("Wonsz", "rzecznyV2"), "1 Update none test failed!")
        self.assertEqual(False, res1, "4 Update incorect return value!!")

        self.add_user(user=self.new_user)
        res2 = self.update_user(user=self.updated)
        self.assertEqual(True, self.verify_user("Wonsz", "rzecznyV2"), "2 Update only test failed!")
        self.assertEqual(True, res2, "3 Update incorect return value!")

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
        self.test_add()
        self.test_remove()
   #     self.test_update()
   #     self.test_thread_safety()


if __name__ == '__main__':
    unittest.main()
