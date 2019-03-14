from Database.DataBase import DataBase
from Database.UsersDatabase import UsersDatabase
import ast
from Processing.DataExtractor import DataExtractor


class InputHandler:
    def __init__(self,
                 db="user"):
        self.DE = DataExtractor()
        self.user_db = UsersDatabase(db)
        self.temp_db = DataBase("temp")
        self.handlers = {
            "/register": lambda data, headers: self.add_user(data),
            "/verify": lambda data, headers: self.verify_user(headers),
            "/download": lambda headers: self.send_databse(headers),
            "/add": lambda data, headers: self.handle_image(data, headers),
        }

    def add_user(self,
                 inp):
        data = self.decode_json(inp)
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
        name, password = self.parse_header(headers)
        if self.user_db.verify_user(password, name):
            return 200
        else:
            return 234

    def send_databse(self,
                     headers):
        name, password = self.parse_header(headers)
        #todo authnticate
        db = self.temp_db.view_database(name + ".json")
        print(db)
        return db

    def handle_image(self,
                     data,
                     headers):  # todo who is sending aka add headers
        with open("test.jpg", 'wb') as f:
            f.write(data)
            self.DE.extract(data)
        # add to database(DE.extact(data))
        return 200

    def decode_json(self,
                    data):
        ret = data.decode('utf-8')
        return ast.literal_eval(ret)

    def get_handlers(self):
        return self.handlers

    def parse_header(self,
                     header):
        authorization = header.get("Authorization")
        creds = authorization.split(':')
        password = creds[1]
        name = creds[0]
        return name, password
