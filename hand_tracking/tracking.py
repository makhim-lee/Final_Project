import cv2
import numpy as np
from multiprocessing import Process, Queue
import detector as detec
import qr_mod as qr
import time

from picamera2 import Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

motion = ""
detector = detec.HandDetector()

queue_input = Queue()
queue_output = Queue()
img_queue = Queue()
stop_value = Queue()
p1 = Process(target=detec.detectorMotion, args=(queue_input,queue_output))
p1.start()
p2 = Process(target=qr.screen_search, args=(img_queue,))
p2.start()

time.sleep(2.0)
cv2.namedWindow("Gotcha")
while True:
    img = picam2.capture_array()
    
    if img_queue.qsize() <= 5:
        img_queue.put(img)
### hand detector    
    detector.findHands(img)
    input_data = detector.findLandmarks(img) 
### motion detector

    if input_data and queue_input.qsize() <= 1:
        queue_input.put(input_data)
    if not queue_output.empty():
        motion = queue_output.get()
        print(motion)
#### air mouse  
    if motion == "Pointer" :
        pointer, img = detector.pointerMouse(img)
        print(pointer)
#### qr and surch screen
#    #qr.start_qr(img)
#    #qr.screen_qr(img)

        
    cv2.imshow("Gotcha", cv2.flip(img, 0))
    
    key = cv2.waitKey(1) 
    if key == ord('q'): 
        stop_value.put(1)
        break
p2.join()
p1.join()
cv2.destroyAllWindows() 