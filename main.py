from DataExtractor import DataExtractor
from PostProcess import PostProcess
from Database.DataBase_unittest import DatabaseTest


def begin():

    ex = DataExtractor("w4a.jpg")

#    ex.showrois()
    post = PostProcess()
    post.getsub(string=ex.extract(threshtype="otsu"))

    return


def main():

    unittest = DatabaseTest()
    unittest.setUp()
    unittest.test_verify()
    unittest.test_add()
    unittest.test_remove()
    unittest.test_update()
    unittest.test_thread_safety()

if __name__ == "__main__":
    main()



