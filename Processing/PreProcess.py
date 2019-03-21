import cv2


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
        if threshtype == "mean":
            thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)[1]
        else:
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
   #     cv2.imshow('captcha_result', thresh)
   #     cv2.waitKey()
        return thresh
