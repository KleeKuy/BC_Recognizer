from Database.DataBase import DataBase
from Database.UsersDatabase import UsersDatabase
import ast
import json
from Processing.DataExtractor import DataExtractor


class InputHandler:
    def __init__(self,
                 db="user"):
        self.DE = DataExtractor()
        self.db = DataBase()
        self.handlers = {
          #  "/register": lambda data, headers: self.add_user(data),
           # "/download": lambda headers: self.send_databse(headers),
            "/add_user": lambda data, headers: self.add_user(data),
            "/remove_user": lambda data, headers: self.remove_user(data, headers),
            "/login": lambda data, headers: self.login(headers),
            "/get_data": lambda headers: self.get_data(headers),    #todo maybe separate get and post callbacks
            "/handle_image": lambda data, headers: self.handle_image(data, headers),
            "/change_password": lambda data, headers: self.change_password(data, headers),
            "/change_data": lambda data, headers: self.change_data(data, headers),
        }

    def add_user(self,
                 inp):
        data = self.decode_json(inp)
        print(data)
        return 200 if self.db.add_user(data['name'], data['password'], data["email"]) else 234

    def change_password(self,
                        data,
                        headers):
        if not self.verify_user(headers):
            return 234
        data = self.decode_json(data)
        name = self.parse_header(headers)[0]
        return 200 if self.db.update_user(name, data['password']) else 234

    def remove_user(self,
                    data,
                    headers):
        data = self.decode_json(data)
        print(data)
        if not self.verify_user(headers):
            return 234
        self.db.remove_user(data['name'])
        return 200

    def login(self,
              headers):
        return 200 if self.verify_user(headers) else 234 #todo return actual user data

    def get_data(self,          #GET
                 headers):
        if not self.verify_user(headers):
            return 234
        name = self.parse_header(headers)[0]
        return self.db.view_database(name)

    def change_data(self,
                    data,
                    headers):
        if not self.verify_user(headers):
            return 234
        data = self.decode_json(data)
        name = self.parse_header(headers)[0]
        return 200 if self.db.update_record(name, data) else 234

    def add_image(self,
                 headers):
        if not self.verify_user(headers):
            return 234
        name = self.parse_header(headers)[0]
        return self.db.view_database(name)

    def verify_user(self,
                    headers):
        name, password = self.parse_header(headers)
        print(name, password)
        #print(self.db.verify_user(password, name))
        return True if self.db.verify_user(name, password) else False

    def handle_image(self,
                     data,
                     headers):
        if not self.verify_user(headers):
            return 234
        user = self.parse_header(headers)[0]

        OCR = self.DE.extract(data)
        self.db.add_record(user, OCR)
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

    #todo remove prints

#{
#    "name":"michau",
#    "email":"michau@mail.com",
#    "password":"pass"
#}