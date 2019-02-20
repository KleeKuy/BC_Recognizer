import json
from enum import Enum


# Users database access modes:
class Mode(Enum):
    VERIFY_USER = 1
    ADD_USER = 2
    UPDATE_USER = 3
    REMOVE_USER = 4


class CONST:
    USERS_DATABSE = "Database/Data/users.json"
    DB_LOCATION = "Database/Data/"
    PASSWORD = "PASSWORD"


class FileIO:

    @staticmethod
    def read_json(file):
        try:
            with open(file) as js:
                return json.loads(js.read())
        except json.decoder.JSONDecodeError:
            print("Json file corrupted!")   #TODO proper error handling
        except FileNotFoundError:
            return json.loads('{}')
        return None

    @staticmethod
    def write_json(file,
                   data):
        with open(file, 'w') as js:
            json.dump(data, js)
