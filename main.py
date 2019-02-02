from DataExtractor import DataExtractor
from PostProcess import PostProcess
from Database.DataBase import DataBase
from Database.Utils import Mode
import json

def begin():

    ex = DataExtractor("w4a.jpg")

#    ex.showrois()
    post = PostProcess()
    post.getsub(string=ex.extract(threshtype="otsu"))

    return


def main():

    def add_user(user): DataBase.access_users(mode=Mode.ADD_USER, user=user)

    def verify_user(user, password): return DataBase.access_users(mode=Mode.VERIFY_USER, user=user, password=password)

    new_user = json.loads(open("Database/new user.json").read())
    add_user(user=new_user)
    updated_user = json.loads(open("Database/updated user.json").read())

    if verify_user("Wonsz", "rzeczny"):
        print("Wonsz verified!")
        db = DataBase("Wonsz")

        def remove_user():
            DataBase.access_users(mode=Mode.REMOVE_USER, user_db=db)

        def update_user(user):
            DataBase.access_users(mode=Mode.UPDATE_USER, user_db=db, user=user)

        update_user(updated_user)
        remove_user()

    else:
        print("unable to verify")


if __name__ == "__main__":
    main()



