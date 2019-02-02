import json
from enum import Enum

USERS_DATABSE = "Database/users.json"


# Users database access modes:
class Mode(Enum):
    VERIFY_USER = 1
    ADD_USER = 2
    UPDATE_USER = 3
    REMOVE_USER = 4


class FileIO:

    @staticmethod
    def read_json(file):
        try:
            with open(file) as js:
                return json.loads(js.read())
        except json.decoder.JSONDecodeError:
            print("Json file corrupted!")   #TODO proper error handling
            return None

    @staticmethod
    def write_json(file,
                   data):
        with open(file, 'w') as js:
            json.dump(data, js)
