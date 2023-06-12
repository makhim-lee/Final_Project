import cv2
import time
import numpy as np
import detector
import threading
from pprint import pprint
cap = cv2.VideoCapture(-1)
detector = detector.HandDetector()

#thread = threading.Thread(target=detector.detectorMotion())
#thread.start()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    
    lm_list = detector.findLandmarks(img) 
    motion = detector.detectorMotion()
    print(motion)
    cv2.imshow("Gotcha", cv2.flip(img, 1))
    
    if cv2.waitKey(1) :
        break

#thread.join()
    