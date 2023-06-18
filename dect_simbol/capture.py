from imutils.video import VideoStream
import imutils
import time
import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
count = 0
directory = 'calib_images/calibration/'
time.sleep(2.0) 

while True:

    frame = picam2.capture_array()
    #frame = imutils.resize(frame, width=1000)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Frame", gray)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("p"):
        filename = directory + 'gray_image_{:02}.jpg'.format(count)
        cv2.imwrite(filename, gray)
        count += 1
        print(count)
    elif key == ord("q"):
        break
    

cv2.destroyAllWindows()
picam2.stop()
