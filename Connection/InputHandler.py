from Database.DataBase import DataBase
from Database.UsersDatabase import UsersDatabase
from Connection.CmdType import CmdType


class InputHandler:
    def __init__(self,
                 db="user"):
        self.user_db = UsersDatabase(db)
        self.db = {}
        self.handlers = {
            CmdType.REGISTER.value: lambda data, ip: self.add_user(data),
            CmdType.VERIFY.value: lambda data, ip: self.verify_user(data, ip),
            CmdType.END.value: lambda ip: self.end_connection(ip=ip),
            CmdType.ADD_RECORD.value: lambda data, ip: self.rec_data(data, ip)
        }

    def add_user(self,
                 data):
        user_data, name = self.parse_user_data(data)
        if name is None:
            return 'F'
        if self.user_db.add_record(user_data):
            return 'T'
        else:
            return 'F'

    def verify_user(self,
                    data,
                    ip):
        print(ip)
        user_data, name = self.parse_user_data(data)
        print(user_data)
        password = user_data[name]["PASSWORD"]
        if self.user_db.verify_user(password, name):
            self.db[ip] = DataBase(name)
            return 'T'
        else:
            return "F"

    def rec_data(self,
                 data,
                 ip):
        client = ip
        print(client)
        test, name = self.parse_user_data(data)
        self.db[client].add_record(test)
        return 'T'

    def end_connection(self,
                       ip):
        print("ending")
        del self.db[ip]         #TODO also this must happen if connection is terminated in any other way

    def parse_user_data(self,
                        data):
        user_data = data.decode('utf-8')
        print(user_data)
        values = (user_data.split('/'))
        pair = []
        dct = {}
        name = None
        for val in values:
            pair.append(val.split(':'))
        i = 0
        for val in pair:
            if val[0] == "NAME":
                name = val[1]
            else:
                dct[val[0]] = val[1]
            i += 1
        if name is None:
            print("Error, no name!")
            return None
        new_user = {name: dct}
        return new_user, name

    def get_handlers(self):
        return self.handlers
