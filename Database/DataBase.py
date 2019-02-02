import threading
from Database.Utils import Mode, USERS_DATABSE, FileIO


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

    @staticmethod
    def update_user(user,
                    user_db):
        DataBase.remove_user(user_db)
        DataBase.add_user(user)
        return

    @staticmethod
    def remove_user(user_db):
        data = FileIO.read_json(USERS_DATABSE)
        del data[user_db.name]
        FileIO.write_json(USERS_DATABSE, data)
        # TODO assert termination of connection, and that db instance is None, add database removal
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
        data = FileIO.read_json(USERS_DATABSE)
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
        data = FileIO.read_json(USERS_DATABSE)
        data.update(user)
        FileIO.write_json(USERS_DATABSE, data)
        return

    @staticmethod
    def access_users(mode,
                     user=None,
                     password=None,
                     user_db=None):
        lock = threading.Lock()
        with lock:
            if mode == Mode.VERIFY_USER:
                return DataBase.verify_user(password, user)
            elif mode == Mode.ADD_USER:
                DataBase.add_user(user)
            elif mode == Mode.UPDATE_USER:
                user_db.update_user(user, user_db)
            elif mode == Mode.REMOVE_USER:
                user_db.remove_user(user_db)
        return
