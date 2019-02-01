from DataExtractor import DataExtractor
from PostProcess import PostProcess
from Database.DataBase import DataBase
import json

def begin():

    ex = DataExtractor("w4a.jpg")

#    ex.showrois()
    post = PostProcess()
    post.getsub(string=ex.extract(threshtype="otsu"))

    return


def main():

    new_user = json.loads(open("Database/new user.json").read())
    DataBase.add_user(new_user)

    if DataBase.verify_user(name="Wonsz", password="rzeczny"):
        #   db = DataBase("Wonsz")
        print("Wonsz verified!")


if __name__ == "__main__":
    main()



