from collections import deque
import cv2
import pyautogui

pyautogui.FAILSAFE = False

Lower = (29, 86, 6)
Upper = (64, 255, 255)
pts = deque(maxlen=64)

camera = cv2.VideoCapture(0)

while True:
    grabbed, frame = camera.read()

    if not grabbed:
        break

    frame = cv2.resize(frame, (800, 600))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, Lower, Upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow('mask', mask)

    con, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(con) > 0:
        c = max(con, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    pts.appendleft(center)

    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(len(pts) / float(i + 1)) * 2
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    if radius < 30:
        pyautogui.moveTo(1366 - 2 * x, 2 * y)
    else:
        x0 = 1366 - (2 * x)
        y0 = 2 * y

    if radius > 40:
        pyautogui.click(x0, y0)

    cmd = str(radius)
    cv2.putText(frame, cmd, (0, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()