import cv2
import time
import numpy as np
import hand_detector as hd
import pyautogui
 
 
wCam, hCam = 640, 480
frameR = 100
smoothening = 7
 
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = hd.handDetector(detectionCon=0.7)
wScr, hScr = pyautogui.size()
print(wScr, hScr)
 
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    output = img.copy()
 
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
 
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (205, 250, 255), -1)
        img = cv2.addWeighted(img, 0.5, output, 1 - .5, 0, output)
 
        # Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
 
            # Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
 
            # Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 6, (255, 28, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY
            # cv2.putText(img, 'Moving Mode', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
 
        # Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
 
            # Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 6, (0, 255, 0), cv2.FILLED)
                # cv2.putText(img, 'Click!!', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                pyautogui.click()
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
 
    cv2.imshow("Vitual mouse monitor", cv2.flip(img, 1))
    cv2.setWindowProperty("Vitual mouse monitor", cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(1)