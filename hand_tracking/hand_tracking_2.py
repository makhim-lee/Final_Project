import cv2
import mediapipe as mp
import time
import threading

def show_frame(img):
    cv2.imshow("Gotcha", img)
    cv2.waitKey(1)

cap = cv2.VideoCapture(-1)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

while True:
    success, img = cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, " :" , cx, cy)
                if id == 0:
                    cv2.circle(img, (cx,cy), 20, (255,0,0), cv2.FILLED)

            mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    threading.Thread(target=show_frame, args=(img,)).start()
    time.sleep(0.001)
