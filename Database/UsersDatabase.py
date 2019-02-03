from Database.DataBase import DataBase
import threading
from Database.Utils import Mode, CONST, FileIO


class UsersDatabase(DataBase):

    def sync_access(self,
                    mode,
                    user,
                    password=None):
        lock = threading.Lock()
        with lock:
            if mode == Mode.VERIFY_USER:
                return self.verify_user(password, user)
            elif mode == Mode.ADD_USER:
                self.add_record(user)
            elif mode == Mode.UPDATE_USER:
                self.update_record(user)
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
            print("unable to verify")
            # self.handle_error()
            return False
        return False
