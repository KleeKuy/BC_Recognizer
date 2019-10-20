from Processing.DataExtractor import DataExtractor


class Tester:
    def __init__(self):
        self.extractor = DataExtractor()

    def test(self):
        with open("SampleImages/fot/1cut.jpg", "rb") as file:
           # with open("smth.jpg", "wb") as f:
           #     f.write(file.read())
            print("Final result is " + str(self.extractor.extract(file.read())))
    #    print(self.extractor.showrois())
