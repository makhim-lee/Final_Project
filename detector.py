
import math
import cv2

from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions.drawing_utils import draw_landmarks
#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import numpy as np
from multiprocessing import Value
import time
class HandDetector():
    def __init__(self, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5): 
        self.hands = mp_hands.Hands(
            #mode= mode, 
            max_num_hands=max_num_hands, 
            min_detection_confidence=min_detection_confidence, 
            min_tracking_confidence=min_tracking_confidence)
         
        self.finger_id = [4, 8, 12, 16, 20]

        self.lm_list = []
        self.results = None
        
    def findHands(self, img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
    
    def findLandmarks(self, img, hand_index=0):
        self.lm_list = []
        input_model_data = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_index]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                #input_model_data.append(round(lm.x, 3), round(lm.y, 3), round(lm.z, 3))
                input_model_data.append(round(lm.x, 3))
                input_model_data.append(round(lm.y, 3))
                input_model_data.append(round(lm.z, 3))
                #input_model_data = np.append(input_model_data, [lm.x,lm.y,lm.z])
                if id == 0:
                    cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
        #input_data = np.array(self.input_model_data).reshape(1,-1)
        #prediction = self.model.predict(input_data)
        return input_model_data
    
    def pointerMouse(self, img):
        pointer = []
        if self.results.multi_hand_landmarks:
            x = self.lm_list[8][1]
            y = self.lm_list[8][2]
            pointer = [x, y]
            cv2.circle(img, (x, y), 6, (0, 255, 255), cv2.FILLED)
        return pointer, img


   
def detectorMotion(queue_input, queue_output):
    model = tf.keras.models.load_model('hand_model.h5')
    flag = 0
    dic_prediction = {
        0: ("Vectory", 1),
        1: ("OK", 2),
        2: ("Pointer",3)
    }
    while True :
        if not queue_input.empty():
            item = queue_input.get()
            
            prediction = model.predict(np.array(item).reshape(1,-1))
            #prediction = model.predict(item)
            for index, (output_string, compare_flag) in dic_prediction.items():
                if prediction[0][index] > 0.9 and flag != compare_flag:
                    queue_output.put(output_string)
                    flag = compare_flag
                    print("input : ", output_string)
                    break
                elif prediction[0][index] > 0.9 :
                    break
            else:
                flag = 0
        
 
if __name__ == "__main__":
    print("OpenCV : ",cv2.__version__)
    print("tensorflow : ",tf.__version__)    