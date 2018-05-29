#import subprocess subprocess.run(["tesseract"], shell=True)
from PIL import Image
import pytesseract
from DataExtractor import DataExtractor
import cv2
from matplotlib import pyplot as plt


def begin():

    ex = DataExtractor("w4a.jpg")
    strings = ex.extracttext()
    for string in strings:
        print(string)
    return


def main():
    begin()


if __name__ == "__main__":
    main()



