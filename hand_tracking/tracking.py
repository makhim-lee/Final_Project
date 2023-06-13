import cv2
import time
import numpy as np
import detector

cap = cv2.VideoCapture(-1)
detector = detector.HandDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lm_list = detector.findLandmarks(img) 
    if lm_list:
        motion = detector.detectorMotion()
        print(motion)
    
    cv2.imshow("Gotcha", cv2.flip(img, 1))
    
    cv2.waitKey(1)

    