import cv2
import numpy as np

class PreProcess:

    def __init__(self):
        pass

    @staticmethod
    def thresh(image,
               threshtype='otsu'):
        print(image)
     #   image = cv2.imread("test.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(threshtype)
     #   if threshtype == "mean":
            #thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)[1]
      #      thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
       # else:
            #thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
           # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 11)
            #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 5)

     #   cv2.imwrite("first.jpg", thresh)
     #   cv2.imwrite("otsu.jpg", otsu)


      #  kernel = np.ones((2, 2), np.uint8)
      #  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
      #  cv2.imwrite("opening.jpg", opening)

    #img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


      #  kernel2 = np.ones((5, 5), np.uint8)
       # close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel2)

      #  cv2.imshow('captcha_result', close)
      #  cv2.waitKey()
      #  cv2.imwrite("treszed.jpg", close)
        return otsu
