import json
import threading

USERS_DATABSE = "Database/users.json"


class DataBase:

    # TODO
    def __init__(self,
                 name):
        self.name = name

    # TODO
    def add_record(self,
                   record,
                   user):
        return

    # TODO
    def remove_record(self,
                      name,
                      user):
        return

    # TODO
    def view_database(self,
                      name):
        return

    # TODO
    def remove_user(self,
                    name,
                    password):
        return

    # TODO
    def change_usr_data(self):
        return

    # TODO
    def view_usr_data(self):
        return

    # TODO
    @staticmethod
    def handle_error():
        print("database error")
        return

    @staticmethod
    def verify_user(password,
                    name):
        with open(USERS_DATABSE, 'r') as js:
            try:
                data = json.loads(js.read())
            except json.decoder.JSONDecodeError:
                DataBase.handle_error()
                return False
            try:
                if data[name]["password"] == password:
                    return True
            except KeyError:
                print("unable to verify")
                # DataBase.handle_error()
                return False
        return False

    @staticmethod
    def add_user(user):
        lock = threading.Lock()  #TODO synchronizing and error handling
        with lock:
            with open(USERS_DATABSE, 'r') as js:
                data = json.loads(js.read())
                data.update(user)
            with open(USERS_DATABSE, 'w') as js:
                json.dump(data, js)
        return
