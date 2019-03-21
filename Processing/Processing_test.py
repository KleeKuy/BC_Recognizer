from Processing.DataExtractor import DataExtractor


class Tester:
    def __init__(self):
        self.extractor = DataExtractor()

    def test(self):
    #    with open("SampleImages/w1.jpg", "rb") as file:
    #        print("Final result is " + str(self.extractor.extract(file.read())))
        print(self.extractor.showrois())
