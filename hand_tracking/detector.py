
import math
import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5): 
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
         
        self.tipIds = [4, 8, 12, 16, 20]
 
        self.lmList = []
        self.results = None
    
    def findHands(self, img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)
        # print(results.multi_hand_landmarks)
 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0):
        xList = []
        yList = []
        self.lmList = []
 
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
 
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
 
                if id == 0:
                    cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
        return self.lmList