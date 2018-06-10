from DataExtractor import DataExtractor
from PostProcess import PostProcess


def begin():

    ex = DataExtractor("w4a.jpg")

#    ex.showrois()
    post = PostProcess()
    post.getsub(string=ex.extract(threshtype="otsu"))

    return


def main():
    begin()


if __name__ == "__main__":
    main()



