import cv2
import numpy as np
from multiprocessing import Process, Queue
import detector as detec
import qr_mod as qr

motion = ""

cap = cv2.VideoCapture(-1)
detector = detec.HandDetector()

queue_input = Queue()
queue_output = Queue()

img_queue = Queue()

p1 = Process(target=detec.detectorMotion, args=(queue_input,queue_output))
p1.start()
#p2 = Process(target=qr.screen_search, args=(img_queue,))
#p2.start()
while True:
    success, img = cap.read()
    #if img_queue.qsize() <= 5:
    #    img_queue.put(img)
### hand detector    
    detector.findHands(img)
    input_data = detector.findLandmarks(img) 
    
### motion detector
    if input_data and queue_input.qsize() <= 3:
        queue_input.put(input_data)
    if not queue_output.empty():
        motion = queue_output.get()
        print(motion)

### air mouse  
    if motion == "Pointer" :
        pointer, img = detector.pointerMouse(img)
        print(pointer)

### qr and surch screen
    qr.start_qr(img)
    qr.screen_qr(img)
    
        
    cv2.imshow("Gotcha", cv2.flip(img, 1))
    
    key = cv2.waitKey(1) 
    if key == ord('q'): 
        queue_input.put(None) 
        break
#p2.join()
p1.join()
cap.release()  
cv2.destroyAllWindows() 