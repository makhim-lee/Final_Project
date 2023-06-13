
import math
import cv2

from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions.drawing_utils import draw_landmarks
#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import numpy as np

import time
class HandDetector():
    def __init__(self, mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5): 
        self.hands = mp_hands.Hands(
            mode, 
            max_num_hands, 
            min_detection_confidence, 
            min_tracking_confidence)
         
        self.finger_id = [4, 8, 12, 16, 20]

        self.lm_list = []
        self.results = None
        
        #self.model = tf.keras.models.load_model('hand_model.h5')
        self.input_model_data = []
    def findHands(self, img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
        return img
    
    def findLandmarks(self, img, hand_index=0):
        self.lm_list = []
        self.input_model_data = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_index]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                self.input_model_data.append([round(lm.x, 3), round(lm.y, 3), round(lm.z, 3)])
                if id == 0:
                    cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
        #input_data = np.array(self.input_model_data).reshape(1,-1)
        #prediction = self.model.predict(input_data)
        return self.lm_list, self.input_model_data
'''
    def detectorMotion(self):
        prediction = []
        #if self.input_model_data :
        input_data = np.array(self.input_model_data).reshape(1,-1)
        prediction = self.model.predict(input_data)
        if prediction[0][0] > 0.9 :
            return "Vectory"
        elif prediction[0][1] > 0.98 :
            return "OK"
        elif prediction[0][2] > 0.9 :
            return "Pointer"
        else : 
            return None
'''

def detectorMotion(queue_input, queue_output):
    model = tf.keras.models.load_model('hand_model.h5')
    flag = 0
    dic_prediction = {
        0: ("Vectory", 1),
        1: ("OK", 2),
        2: ("Pointer",3)
    }
    while(True):
        if not queue_input.empty():
            item = queue_input.get()
            if item is None:
                break
            prediction = model.predict(np.array(item).reshape(1,-1))
             
            for index, (output_string, compare_flag) in dic_prediction.items():
                if prediction[0][index] > 0.9 and flag != compare_flag:
                    queue_output.put(output_string)
                    flag = compare_flag
                    break
                elif prediction[0][index] > 0.9 :
                    break
            else:
                flag = 0
            '''
            
            
            if prediction[0][0] > 0.9 and not flag == 1:
                queue_output.put("Vectory")
                flag = 1
            elif prediction[0][1] > 0.98 and not flag == 2:
                queue_output.put("OK")
                flag = 2
            elif prediction[0][2] > 0.9 and not flag == 3:
                queue_output.put("Pointer")
                flag = 3
            else:
                flag = 0            
            '''            


        
        
 
if __name__ == "__main__":
    print("OpenCV : ",cv2.__version__)
    print("tensorflow : ",tf.__version__)    
    #def fingersCheck(self):
    #    fingers = []
    #    fingers.append(1 if self.lm_list[self.finger_id[0]][1] < self.lm_list[self.finger_id[0] - 2][1] \
    #        else 0)
    #    fingers = [1 if self.lm_list[self.finger_id[id]][2] < self.lm_list[self.finger_id[id] - 2][2] \
    #        else 0 \
    #            for id in range(1,5)]
    #    
    #    return fingers
    # 
    #def calculateDistance(self, p1, p2, img):
    #    x1, y1 = self.lm_list[p1][1:]
    #    x2, y2 = self.lm_list[p2][1:]
    #    
    #    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
    #    cv2.circle(img, (x1, y1), 6, (0, 255, 255), cv2.FILLED)
    #    cv2.circle(img, (x2, y2), 6, (0, 255, 255), cv2.FILLED)
 #
    #    length = math.hypot(x2 - x1, y2 - y1)
 #
    #    return length, img, [x1, y1, x2, y2]
 