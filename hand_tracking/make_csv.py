import pandas as pd
import cv2
import time
import numpy as np
import detector
from pprint import pprint
cap = cv2.VideoCapture(-1)
detector = detector.HandDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    
    lm_list,save_list = detector.findLandmarks(img) 
    if cv2.waitKey(1) & 0xFF == ord('p'):#(lm_list is not None):
        df = pd.DataFrame(save_list)
        print(df)
        df.to_csv("landmarks.csv",header=None, index=None)   
    cv2.imshow("Gotcha", cv2.flip(img, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()