import cv2
import pytesseract
from Processing.PreProcess import PreProcess
from Processing.PostProcess import PostProcess
import numpy as np
import re


class DataExtractor:

    def extract(self,
                data):
        decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
        # Proprocessing
        threshed = PreProcess.thresh(image=decoded)
        # Tesseract processing
        res = pytesseract.image_to_string(lang='pol', image=threshed)
        # Postprocessing
        fin = PostProcess(res).get_record()
        return fin

    def showrois(self,  #zdetekować wszystko jako jeden duży jak jest fuży gradient na rogach
                 threshtype="otsu",
                 kernel=cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)),
                 iterations=5):
        image = cv2.imread("SampleImages/w3.jpg")
        thresh = PreProcess.thresh(image=image)
        dilated = cv2.dilate(thresh, kernel, iterations=iterations)
        img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        clipped = []
        for contour in contours:
            print(cv2.boundingRect(contour))
            [x, y, w, h] = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            clipped.append(image[y:y+h, x:x+w])
        # cv2.imshow('captcha_result', image)
        # cv2.waitKey()

        return self.handle_clipped(clipped)

    def handle_clipped(self,
                       clipped):
        ret = []
        for img in clipped:
            text = pytesseract.image_to_string(lang='pol', image=img)
            s = re.findall(r"\d", text)
            if s is not None:
                if len(s) > 8:
                    string = "".join(s)
                    ret.append(string)
        return ret




