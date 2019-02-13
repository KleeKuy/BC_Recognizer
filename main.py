from DataExtractor import DataExtractor
from PostProcess import PostProcess
from Database.DataBase_unittest import DatabaseTest
from Connection.WebHandler_unittest import WebServetTest


def begin():

    ex = DataExtractor("w4a.jpg")

#    ex.showrois()
    post = PostProcess()
    post.getsub(string=ex.extract(threshtype="otsu"))

    return


def main():
    #unittestdb = DatabaseTest()
    #unittestdb.run_all()
    unittestweb = WebServetTest()
    unittestweb.run_all()


if __name__ == "__main__":
    main()



