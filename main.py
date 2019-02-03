from DataExtractor import DataExtractor
from PostProcess import PostProcess
from Database.DataBase import DataBase
from Database.Utils import Mode, CONST
from Database.UsersDatabase import UsersDatabase
import json


def begin():

    ex = DataExtractor("w4a.jpg")

#    ex.showrois()
    post = PostProcess()
    post.getsub(string=ex.extract(threshtype="otsu"))

    return


def main():

    USER = "Wonsz"
    password = "rzeczny"

    users_db = UsersDatabase("users")

    def add_user(user): users_db.sync_access(mode=Mode.ADD_USER, user=user)

    def verify_user(user, password): return users_db.sync_access(mode=Mode.VERIFY_USER, user=user, password=password)

    def update_user(user): users_db.sync_access(mode=Mode.UPDATE_USER, user=user)

    def remove_user(user): users_db.sync_access(mode=Mode.REMOVE_USER, user=user)

    new_user = json.loads(open("Database/Data/new user.json").read())
    add_user(user=new_user)
    updated_user = json.loads(open("Database/Data/updated user.json").read())

    if verify_user(USER, password):
        print("Wonsz verified!")
        #db = DataBase("Wonsz")

        update_user(updated_user)
        #remove_user("Wonsz")
    else:
        print("unable to verify")

    db = DataBase(USER)
    BC1 = json.loads(open(CONST.DB_LOCATION + "BC1.json").read())
    BC2 = json.loads(open(CONST.DB_LOCATION + "BC2.json").read())
    db.add_record(BC1)
    db.add_record(BC2)

if __name__ == "__main__":
    main()



