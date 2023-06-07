import cv2
import time
import numpy as np
import detector


cap = cv2.VideoCapture(-1)
detector = detector.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    imList = detector.findPosition(img) 
    cv2.imshow("Gotcha", cv2.flip(img, 1))
    cv2.waitKey(1)
    
    