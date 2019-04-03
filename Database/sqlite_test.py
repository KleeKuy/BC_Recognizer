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
        #self.test_add_user()
        #self.test_add_record()
        self.test_remove_user()

     #   name = "Radovid"
     #   data = {"smth":"2",
     #           "moar":"yas"}
     #   db.add_record(name, data)
      #  res = db.view_database("Bob Girlyman")
       # print(res.fetchone())

    def test_ver(self):
        res = self.db.verify_user("Radovid", "20pointsShani")
        print(res)

    def test_add_user(self):
        name = "Indrick Boreale"
        password = "SpessMehrens"
        res = self.db.add_user(name, password)
        print(res)

    def test_update(self):
        self.db.update_user("test", "silver")

    def test_add_record(self):
        rec = {"Marneus": {"password": "1v1meHibrTyrant", "email": "ChapterMaster@ultramar.org"}}
        js = json.dumps(rec)
        self.db.add_record(data=js, name="Bob Gyrlyman")

    def test_remove_user(self):
        self.db.remove_user("test")
