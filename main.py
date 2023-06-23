import cv2
import numpy as np
from multiprocessing import Process, Queue, Event
import detector as detec

import time
from multi_proc_not_socket import mark_detec
import os

from picamera2 import Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
time.sleep(2.0)

motion = ""
perv_motion = None
pointer = None
far_flag = True
detector = detec.HandDetector()
stop_event = Event()

queue_input = Queue()
queue_output = Queue()
#p1 = Process(target=detec.detectorMotion, args=(
#    queue_input, queue_output, stop_event))
#p1.start()

motion_Q = Queue()
img_queue = Queue()
p2 = Process(target=mark_detec, args=(img_queue, motion_Q, stop_event))
p2.start()


while not stop_event.is_set():
    img = picam2.capture_array()

# hand detector
    detector.findHands(img)
    input_data = detector.findLandmarks(img)
# motion detector
    if input_data and queue_input.qsize() <= 1:
        queue_input.put(input_data)
    if not queue_output.empty():
        motion = queue_output.get()
# air mouse
    distance = detector.distanceHand()
    if distance < 166 and far_flag:
        motion_Q.put("far")
        far_flag = False
    elif distance > 166:
        far_flag = True
    
    motion = "Pointer"
    if (motion == "Pointer") :
        motion = detector.pointerMouse(img)
        
    if motion != perv_motion and motion_Q.qsize() <= 3:
        motion_Q.put(motion)
        perv_motion = motion
        
    if img_queue.qsize() <= 3:
        img_queue.put(img)

    # cv2.imshow("Gotcha", cv2.flip(img, 1))

time.sleep(1)
p2.join()
#p1.join()
picam2.stop()
os._exit(0)
