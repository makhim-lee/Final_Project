import cv2
import numpy as np

def detect_shape(contour):
    shape = "unidentified"
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

    if len(approx) == 3:
        shape = "triangle"
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        center = [x + w/2, y + h/2]
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    elif len(approx) > 4:
        shape = "circle"
        
    return shape

cap = cv2.VideoCapture(-1)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    
    _,contours,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        shape = detect_shape(contour)
        if shape != "unidentified" and shape == "square":
            
            c = contour.astype("int")
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 1)

    cv2.imshow("Image", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
