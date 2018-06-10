import cv2
import pytesseract

class DataExtractor:
    def __init__(self,
                 filename):
        self.filename = filename
        self.image = cv2.imread(filename)

    def setfile(self,
                filename):
        self.filename = filename

    def preprocess(self,
                   threshtype):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        if threshtype == "mean":
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)[1]
        else:
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        return thresh

    def showrois(self,  #zdetekować wszystko jako jeden duży jak jest fuży gradient na rogach
                 threshtype="otsu",
                 kernel=cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5)),
                 iterations=5):
        thresh = self.preprocess(threshtype)
        dilated = cv2.dilate(thresh, kernel, iterations=iterations)
        img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            print(cv2.boundingRect(contour))
            [x, y, w, h] = cv2.boundingRect(contour)
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 255), 2)

        cv2.imshow('captcha_result', self.image)
        cv2.waitKey()
        return

    def extract(self,
                threshtype="otsu"):
        self.preprocess(threshtype)
        return pytesseract.image_to_string(lang='pol', image=self.image)





