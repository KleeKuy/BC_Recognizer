import sqlite3
import json

DB_FILENAME = "Database/Data/database.db"


class SqlInterface:

    def __init__(self):
        self.connection = sqlite3.connect(DB_FILENAME)
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS user (
            username TEXT,
            password TEXT,
            email    TEXT,
            data     JSON
        )
        """)
        self.connection.commit()

    """ Returns record from database
    @:param ret - str value, it is name of column from which return value will be retrieved
    @:param user - str value that specifies record to return
    """
    def select(self,
               ret,
               user):
     #   print(self.print_all())
        res = self.connection.execute("SELECT " + ret + " FROM user WHERE username='" + user + "'")
        if res.arraysize is not 1:
            print("Sommething went wrong in SqlInterface.select()!")
            return None
        else:
            return res

    """ Inserts to database new values
    @:param name - str value that sepcufies new username
    @:param password - str value that specifies new password
    """
    def insert(self,
               name,
               password,
               email=None,
               data=None):
        json_data = json.dumps(data)
        self.connection.execute("""
        INSERT INTO user (username, password, email, data)
        VALUES (?, ?, ?, ?)
        """, (name, password, email, json_data))
        self.connection.commit()

    """ Updates record in user table 
    @param value - dict object that represents updates to user table, e.g {column: new_value, column2: new_value2...}
    All those updates are applied to user with username equal to username parameter
    @param name - str that specifies user record that will be updated
    """
    def update(self,
               value,
               name):
        val, querry = self.prepare_update_querry(value, name)
        self.connection.execute("""""" + querry + """""", val)
        self.connection.commit()

      #  self.print_all()

    def delete(self,
               name):
     #   print(name)
        self.connection.execute("""
        DELETE FROM user WHERE username = ?
        """, (name,))
        self.connection.commit()
      #  print(self.print_all())

    def prepare_update_querry(self,
                              update,
                              name):
        querry = "UPDATE user SET username = ?"
        values = [name]
        for up in update:
            querry += ", " + up + " = ?"
         #   print(str(up))
            values.append(update[up])
        querry += " WHERE username is ?"
        values.append(name)
      #  print(values)
       # print(querry)
        return values, querry

    def print_all(self):
        for row in self.connection.execute("SELECT * FROM user"):
            print(row)
