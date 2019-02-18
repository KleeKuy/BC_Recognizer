from Database.Utils import FileIO, CONST


class DataBase:

    def __init__(self,
                 name):
        self._name = name
        self._file = CONST.DB_LOCATION + name + ".json"

    # TODO
    def view_database(self,
                      name):
        return

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

    def add_record(self,
                   record):
        data = FileIO.read_json(self._file)
        name = (next(iter(record.keys())))
        try:
            if data[name] is not None:
                print("record already exists!")
                return False
        except KeyError:
            data.update(record)
            FileIO.write_json(self._file, data)
            return True

    # TODO
    @staticmethod
    def handle_error():
        print("database error")
        return
