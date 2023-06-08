
import math
import cv2

from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions.drawing_utils import draw_landmarks

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
    
    def findHands(self, img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)
 
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
        return img
    
    def findLandmarks(self, img, hand_index=0):
        self.lm_list = []
        save_list = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_index]
 
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                
                save_list.append([format(lm.x,'.3f'), format(lm.y,'.3f'), format(lm.z,'.3f')])
                if id == 0:
                    cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
        return self.lm_list, save_list
    
    def fingersCheck(self):
        fingers = []
        fingers.append(1 if self.lm_list[self.finger_id[0]][1] < self.lm_list[self.finger_id[0] - 2][1] \
            else 0)
        fingers = [1 if self.lm_list[self.finger_id[id]][2] < self.lm_list[self.finger_id[id] - 2][2] \
            else 0 \
                for id in range(1,5)]
        
        return fingers
     
    def calculateDistance(self, p1, p2, img):
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
        cv2.circle(img, (x1, y1), 6, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 6, (0, 255, 255), cv2.FILLED)
 
        length = math.hypot(x2 - x1, y2 - y1)
 
        return length, img, [x1, y1, x2, y2]
 