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
    #unittestdb.setUp()
    #unittestdb.test_add()
    #unittestdb.run_all()
    unittestweb = WebServetTest()
    unittestweb.test()


if __name__ == "__main__":
    main()



