import cv2
import time
import numpy as np
import detector
from pprint import pprint
cap = cv2.VideoCapture(-1)
detector = detector.HandDetector()
prev_fingers= None


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    
    lm_list = detector.findLandmarks(img) 
    if len(lm_list) != 0 :
        fingers = detector.fingersCheck()
        pprint(fingers)
        if fingers[1] == 1 and fingers[2] == 1 :
            length, img, linInfo = detector.calculateDistance(8, 12, img) 

    cv2.imshow("Gotcha", cv2.flip(img, 1))
    cv2.waitKey(1)
    
    