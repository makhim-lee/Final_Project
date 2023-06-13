import cv2 


cap = cv2.VideoCapture(-1)

while True:
    success, img = cap.read()
    

    cv2.imshow("Gotcha", cv2.flip(img, 1))
    
    cv2.waitKey(1)
        
