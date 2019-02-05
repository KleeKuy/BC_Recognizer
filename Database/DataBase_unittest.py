import unittest
from Database.UsersDatabase import UsersDatabase
from Database.Utils import Mode
import json
import os
from threading import Thread


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        users_db = UsersDatabase("test")
        self.verify_user = lambda user, password: users_db.sync_access(mode=Mode.VERIFY_USER, user=user,
                                                                       password=password)
        self.add_user = lambda user: users_db.sync_access(mode=Mode.ADD_USER, user=user)
        self.update_user = lambda user: users_db.sync_access(mode=Mode.UPDATE_USER, user=user)
        self.remove_user = lambda user: users_db.sync_access(mode=Mode.REMOVE_USER, user=user)
        self.new_user = json.loads(open("Database/Data/new user.json").read())
        self.new_user2 = json.loads(open("Database/Data/new user2.json").read())
        self.updated = json.loads(open("Database/Data/updated user.json").read())
        self.test_loc = "Database/Data/test.json"

    def test_verify(self):
        self.assert_no_db()
        self.add_user(user=self.new_user)
        self.assertEqual(True, self.verify_user("Wonsz", "rzeczny"), "1 Verify true test failed!")
        self.add_user(user=self.new_user)
        self.assertEqual(False, self.verify_user("Wonsz", "rzeczn"), "2 Verify false test failed!")
        self.add_user(user=self.new_user)
        self.assertEqual(False, self.verify_user("onsz", "rzeczny"), "3 Verify false test failed!")

    def test_add(self):
        self.assert_no_db()
        self.add_user(user=self.new_user)
        self.assertEqual(True, self.verify_user("Wonsz", "rzeczny"), "1 Add to new db test failed!")

        self.add_user(user=self.new_user2)
        self.assertEqual(True, self.verify_user("Wonsz", "rzeczny"), "2 Add to existing db test failed!")
        self.assertEqual(True, self.verify_user("Wonsz2", "rzeczny2"), "3 Add to existing db test failed!")

        self.remove_user("Wonsz")
        self.remove_user("Wonsz2")
        self.add_user(user=self.new_user)
        self.assertEqual(True, self.verify_user("Wonsz", "rzeczny"), "4 Add to empty db test failed!")

    def test_remove(self):
        self.assert_no_db()
        self.add_user(user=self.new_user)
        self.remove_user("Wonsz")
        self.assertEqual(False, self.verify_user("Wonsz", "rzeczny"), "1 Remove only record test failed!")

        self.add_user(user=self.new_user)
        self.add_user(user=self.new_user2)
        self.remove_user("Wonsz")
        self.assertEqual(False, self.verify_user("Wonsz", "rzeczny"), "2 Remove one record test failed!")
        self.remove_user("Wonsz2")
        self.assertEqual(False, self.verify_user("Wonsz2", "rzeczny2"), "3 Remove second record test failed!")

        self.remove_user("Wonsz")
        self.assertEqual(False, self.verify_user("Wonsz", "rzeczny"), "4 Remove not existing record test failed!")

    def test_update(self):
        self.assert_no_db()
        self.update_user(user=self.updated)
        self.assertEqual(False, self.verify_user("Wonsz", "rzecznyV2"), "1 Update none test failed!")

        self.add_user(user=self.new_user)
        self.update_user(user=self.updated)
        self.assertEqual(True, self.verify_user("Wonsz", "rzecznyV2"), "2 Update only test failed!")

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

    def assert_no_db(self):
        try:
            os.remove(self.test_loc)
        except FileNotFoundError:
            return

    def run_all(self):
        self.test_verify()
        self.test_add()
        self.test_remove()
        self.test_update()
        self.test_thread_safety()


if __name__ == '__main__':
    unittest.main()
