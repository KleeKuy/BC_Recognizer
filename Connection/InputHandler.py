from Database.DataBase import DataBase
from Database.UsersDatabase import UsersDatabase
from Connection.CmdType import CmdType


class InputHandler:
    _instance = None

    def __init__(self,
                 db="user"):
        self.user_db = UsersDatabase(db)
        self.db = {}
        self.handlers = {
            "/register": lambda data, headers: self.add_user(data),
            "/verify": lambda data, headers: self.verify_user(headers),
            CmdType.ADD_RECORD.value: lambda data, ip: self.rec_data(data, ip)
        }

    def add_user(self,
                 data):
        record = {
            data["name"]: {"EMAIL": data["email"],
                           "PASSWORD": data["password"]}
        }
        if self.user_db.add_record(record):
            return 200
        else:
            return 234

    def verify_user(self,
                    headers):
        authorization = headers.get("Authorization")
        creds = authorization.split(':')
        password = creds[1]
        name = creds[0]
        if self.user_db.verify_user(password, name):
            self.db[name] = DataBase(name)
            return 200
        else:
            return 234

    def rec_data(self,
                 data,
                 ip):
        client = ip
        print(client)
        test, name = self.parse_user_data(data)
        self.db[client].add_record(test)
        return 'T'

    def get_handlers(self):
        return self.handlers
