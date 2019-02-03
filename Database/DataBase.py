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
        self.remove_record(next(iter(record.keys())))
        self.add_record(record)
        return

    def remove_record(self,
                      record):
        data = FileIO.read_json(self._file)
        del data[record]
        FileIO.write_json(self._file, data)
        # TODO assert termination of connection, and that db instance is None, add database removal
        return

    def add_record(self,
                   record):
        data = FileIO.read_json(self._file)
        data.update(record)
        FileIO.write_json(self._file, data)
        return

    # TODO
    @staticmethod
    def handle_error():
        print("database error")
        return
