import sqlite3
import json
from Database.DataBase import DataBase

DB_FILENAME = "Database/Data/database.db"


class sqlite_test:

    def __init__(self):
        self.db = DataBase()

    def connect(self):
        self.connection = sqlite3.connect(DB_FILENAME)

    def do_stuff(self):
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS user (
            username TEXT,
            password TEXT,
            email    TEXT,
            data     JSON
        )
        """)
        self.connection.commit()

        some_data = {"sample": "raz",
                     "cos": "cosjescze"}
        jobject = json.dumps(some_data)

        self.connection.executemany("""
        INSERT INTO user (username, password, email, data)
        VALUES (?, ?, ?, ?)
        """, (('wonsz_rzeczny', 'jest_niebezpieczny', "wonsz@rzeka.com", jobject),
              ('Radovid', '20pointsShani', "Radovid@africa.com", jobject)))
        self.connection.commit()

        for row in self.connection.execute("SELECT * FROM user"):
            print(row)

    def test(self):
        self.test_add_user()
        self.test_remove_user()
        self.test_ver()
        self.test_remove_record()
        self.test_add_record()
        self.test_update_record()


    #   name = "Radovid"
     #   data = {"smth":"2",
     #           "moar":"yas"}
     #   db.add_record(name, data)
      #  res = db.view_database("Bob Girlyman")
       # print(res.fetchone())

    def test_ver(self):
        name = "Indrick Boreale"
        password = "SpessMehrens"
        self.db.add_user(name, password)
        res = self.db.verify_user("Indrick Boreale", "SpessMehrens")
        if res is True:
            print("!!! 1ver test passed")
        else:
            print("!!! 1ver test failed")

        self.db.remove_user("Indrick Boreale")
        res = self.db.verify_user("Indrick Boreale", "SpessMehrens")
        if res is False:
            print("!!! 2ver test passed")
        else:
            print("!!! 2ver test failed")

    def test_add_user(self):
        self.db.remove_user("Indrick Boreale")
        name = "Indrick Boreale"
        password = "SpessMehrens"
        self.db.add_user(name, password)
        res = self.db.verify_user("Indrick Boreale", "SpessMehrens")
        print("res val is " + str(res))
        if res is True:
            print("!!!add  user test passed")
        else:
            print("!!!add  user test failed")

    def test_update(self):
        self.db.update_user("test", "silver")

    def test_remove_user(self):
        self.db.remove_user("Indrick Boreale")
        self.db.remove_user("Indrick Boreale")
        res = self.db.verify_user("Indrick Boreale", "SpessMehrens")
        if res is False:
            print("!!!remove test passed")
        else:
            print("!!!remove test failes=d")

    def test_add_record(self):
        name = "Bob Gyrlyman"
        dataname = "Marneus"
        rec = {dataname: {"password": "1v1meHibrTyrant", "email": "ChapterMaster@ultramar.org"}}
        js = json.dumps(rec)
        self.db.add_record(data=js, name=name)
        self.db.add_record(data=js, name=name)
        db = self.db.view_database(name)
        if db[dataname] == rec[dataname]:
            print("!!!1 add record test passed")
        else:
            print("!!!1 add record test failed")

        self.db.remove_record(name, dataname)
        self.db.add_record(data=js, name=name)
        db = self.db.view_database(name)
        if db[dataname] == rec[dataname]:
            print("!!!2 add record test passed")
        else:
            print("!!!2 add record test failed")

    def test_update_record(self):
        name = "Bob Gyrlyman"
        dataname = "Marneus"
        rec = {dataname: {"password": "1v1meHibrTyrant", "email": "ChapterMaster@ultramar.org"}}
        js = json.dumps(rec)
        self.db.add_record(data=js, name=name)
        up = {dataname: {"password": "alpahriusdidnthackme", "email": "notevenalpharius@ultramar.org"}}
        self.db.update_record(name, up)
        res = self.db.view_database(name)
        if res[dataname] == up[dataname]:
            print("!!! update record test passed")
        else:
            print("!!! update record test failed")

    def test_remove_record(self):
        name = "Bob Gyrlyman"
        dataname = "Marneus"
        rec = {dataname: {"password": "1v1meHibrTyrant", "email": "ChapterMaster@ultramar.org"}}
        js = json.dumps(rec)
        self.db.add_record(data=js, name=name)
        print("remove")
        self.db.remove_record(name, dataname)
        self.db.remove_record(name, dataname)
        db = self.db.view_database("Bob Gyrlyman")
        try:
            db[dataname]
        except KeyError:
            print("!!! remove record test pass")
            return
        print("!!! remove record test failed")
