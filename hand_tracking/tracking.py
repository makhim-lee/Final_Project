import cv2
import numpy as np
from multiprocessing import Process, Queue
import detector as detec
import qr_mod as qr

cap = cv2.VideoCapture(-1)
detector = detec.HandDetector()

queue_input = Queue()
queue_output = Queue()

p1 = Process(target=detec.detectorMotion, args=(queue_input,queue_output))
p1.start()

while True:
    success, img = cap.read()
    qr.screen_qr(img)
    img = detector.findHands(img)
    lm_list, input_data = detector.findLandmarks(img) 
    #if lm_list:
    #    motion = detector.detectorMotion()
    #    print(motion)
    if input_data:
        queue_input.put(input_data)
    if not queue_output.empty():
        motion = queue_output.get()
        print(motion)
    cv2.imshow("Gotcha", cv2.flip(img, 1))
    
    key = cv2.waitKey(1) 
    if key == ord('q'): 
        queue_input.put(None) 
        break

p1.join()
cap.release()  
cv2.destroyAllWindows() 