from Database.Utils import FileIO, CONST
from Database.SqlInterface import SqlInterface
import json
import ast


class DataBase:

    def __init__(self):
        self._sql = SqlInterface()

    def view_database(self,                 #todo this function name seems to be abit misleading
                      name):
        data = self._sql.select("data", name).fetchone()[0]     #todo seems to not work whern there is no data
        if data == 'null':
            return None
        print("this is the data")
        print(data)
        ret = ast.literal_eval(data)
        if isinstance(ret, dict):
            return ret
        else:
            return ast.literal_eval(ret)

    def verify_user(self,
                    name,
                    password):
        res = self._sql.select("password", name)
        print(res)
        rec = res.fetchone()
        print("rec is " + str(rec)) #TODO remove or smth
        if rec is not None:
            correct_pass = rec[0]
        else:
            return False
        if password == correct_pass:
            return True
        else:
            return False

    def add_user(self,
                 name,
                 password,
                 email):
        res = self._sql.select("username", name)
        if res.fetchone() is None:
            self._sql.insert(name, password, email)
            return True
        else:
            return False

    def update_user(self,
                    name,
                    password):
        update = {"password": password}
        self._sql.update(update, name)

    def remove_user(self,
                    name):
        self._sql.delete(name)

    """ Adds record to database
    @:param name - str, user name
    @:param data - dict, new record to add
    """
    def add_record(self,
                   name,
                   data):
        db = self.view_database(name)
        try:
            if db is not None:
                db.update(data)
            else:
                db = data
            final = json.dumps(db)
            update = {"data": final}
        except TypeError:
            update = {"data": data}
        self._sql.update(value=update, name=name)
        return True     #todo

    def remove_record(self,
                      name,
                      record_name): #todo idk we can maybe make it consistent, but also we pass redundand data then>
        db = self.view_database(name)
        try:
            del db[record_name]
            self.update_data_sql(name, db)
        except KeyError:
            print("there is no such record, therefore cannot be deleted!")

    def update_record(self,
                      name,
                      record):
        db = self.view_database(name)
        record_name = (next(iter(record.keys())))
        try:
            db[record_name] = record[record_name]
            self.update_data_sql(name, db)
            return True
        except KeyError:
            print("there is no such record, therefore cannot be updated!")
            return False

    def update_data_sql(self,
                        name,
                        db):
        js = json.dumps(db)
        update = {"data": js}
        self._sql.update(value=update, name=name)
