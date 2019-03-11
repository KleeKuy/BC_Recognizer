from Database.DataBase import DataBase
from Database.UsersDatabase import UsersDatabase
from Connection.CmdType import CmdType


class InputHandler:
    _instance = None

    def __init__(self,
                 db="user"):
        self.user_db = UsersDatabase(db)
        self.temp_db = DataBase("temp")
        self.handlers = {
            "/register": lambda data, headers: self.add_user(data),
            "/verify": lambda data, headers: self.verify_user(headers),
            "/download": lambda headers: self.get_databse(headers),
            "/add": lambda data, headers: self.handle_image(data),
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
     #       self.db[name] = DataBase(name)
            return 200
        else:
            return 234

    def get_databse(self,
                    headers):
        print("here we are")
        authorization = headers.get("Authorization")    #todo redundancy
        if authorization is None:
            return {"zledales": "hasloitditp"}
        creds = authorization.split(':')
        password = creds[1]
        name = creds[0]
        #todo authnticate
        db = self.temp_db.view_database(name + ".json")
        print(db)
        return db

    def handle_image(self,
                     data):
        print("we got ourselve an imge POG")

        with open("test", 'wb') as f:
            f.write(data)

        return 200

    def get_handlers(self):
        return self.handlers
