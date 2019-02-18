from Database.DataBase import DataBase
from threading import Lock
from Database.Utils import Mode, CONST, FileIO


class UsersDatabase(DataBase):

    def __init__(self,
                 name):
        DataBase.__init__(self, name)
        self._lock = Lock()

    def sync_access(self,
                    mode,
                    user,
                    password=None):
        with self._lock:
            if mode == Mode.VERIFY_USER:
                return self.verify_user(password, user)
            elif mode == Mode.ADD_USER:
                return self.add_record(user)
            elif mode == Mode.UPDATE_USER:
                return self.update_record(user)
            elif mode == Mode.REMOVE_USER:
                self.remove_record(user)
        return

    def verify_user(self,
                    password,
                    name):
        data = FileIO.read_json(self._file)
        try:
            if data[name][CONST.PASSWORD] == password:
                return True
        except KeyError:
            print("unable to verify")   # TODO
            # self.handle_error()
            return False
        return False
