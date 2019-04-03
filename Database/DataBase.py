from Database.Utils import FileIO, CONST
from Database.SqlInterface import SqlInterface
import json


class DataBase:

    def __init__(self):
        self._sql = SqlInterface()

    def view_database(self,
                      name):
        return self._sql.select("data", name)

    def verify_user(self,
                    name,
                    password):
        res = self._sql.select("password", name)
        if res.fetchone() is not None:
            correct_pass = res.fetchone()[0]
        else:
            return False
        if password == correct_pass:
            return True
        else:
            return False

    def add_user(self,
                 name,
                 password):
        res = self._sql.select("username", name)
        if res.fetchone() is None:
            self._sql.insert(name, password)
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


    def add_record(self,
                   name,
                   data):
        db = self._sql.select("data", name)
        existing = json.loads(db.fetchone()[0])
        new = json.loads(data)
        try:
            existing.update(new)
            final = json.dumps(existing)
            update = {"data": final}
        except TypeError:
            update = {"data": data}
        self._sql.update(value=update, name=name)
        return True #todo

    def update_record(self,
                      record):
        name = (next(iter(record.keys())))
        data = FileIO.read_json(self._file)
        try:
            if data[name] is not None:
                data.update(record)
                FileIO.write_json(self._file, data)
                return True
        except KeyError:
            print("No such record!")    # TODO
            return False

    def remove_record(self,
                      record):
        data = FileIO.read_json(self._file)
        try:
            del data[record]
        except KeyError:
            print("No such record!")    # TODO
            return False
        FileIO.write_json(self._file, data)
        # TODO assert termination of connection, and that db instance is None, add database removal
        return True

    # TODO
    @staticmethod
    def handle_error():
        print("database error")
        return
