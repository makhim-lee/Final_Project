import cv2
import numpy as np
from multiprocessing import Process, Queue, Event


import time

import os

from picamera2 import Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()


motion = ""
perv_motion = None
pointer = None
far_flag = True
stop_event = Event()

import detector as detec
detector = detec.HandDetector()
queue_input = Queue()
queue_output = Queue()
p1 = Process(target=detec.detectorMotion, args=(queue_input, queue_output, stop_event))
p1.start()

#from multi_proc_not_socket import mark_detec
from multi_proc_mod import mark_detec
motion_Q = Queue()
img_queue = Queue()
p2 = Process(target=mark_detec, args=(img_queue, motion_Q, stop_event))
p2.start()

#from searching2 import assistant_proc
#yolo_event = Event()
#yolo_Q = Queue()
#p3 = Process(target=assistant_proc, args=(yolo_Q, ))

while True:
    try:
        
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
        #distance = detector.distanceHand()
        #if isinstance(distance, str) and motion_Q.qsize() <= 1:
        #    motion_Q.put(distance)
        #    distance = None
    
        if (motion == "Pointer") or isinstance(motion, list) :
            motion = detector.pointerMouse(img)

        if motion != perv_motion and motion_Q.qsize() <= 1:
            motion_Q.put(motion)
            perv_motion = motion
        ### detec obj with yolo
            #if motion == "Good":
            #    p3.start()
            #    print("start, assistant")
            #    #yolo_event.set()
            #    time.sleep(1)
            #    for _ in range(3):
            #        time.sleep(3)
            #        print("plz, wait 3sec")
            #        img = picam2.capture_array()
            #        yolo_Q.put(img)
            #        img_queue.put(img)
            #    motion = ""

             #cv2.imshow("Gotcha", cv2.flip(img, 1))

        if img_queue.qsize() <= 5:
            img_queue.put(img)
            
    except KeyboardInterrupt:
        stop_event.set()
        print("error")
        time.sleep(1)
        #p3.join()
        p2.join()
        p1.join()
        picam2.stop()
        os._exit(0)

