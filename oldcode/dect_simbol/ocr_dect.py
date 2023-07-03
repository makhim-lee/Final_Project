import time
import numpy as np
import cv2
import pytesseract
    

# Capture video from the webcam
cap = cv2.VideoCapture(-1)

while True:
    # Read the current frame
    ret, frame = cap.read()

    if ret:
        # Convert the image from BGR to RGB
        #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grey to reduce detials 
        gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
        
        original = pytesseract.image_to_string(gray, config='')
        # Use Tesseract to find text in the image
        #data = pytesseract.image_to_data(frame_rgb, output_type=pytesseract.Output.DICT)
        #text = pytesseract.image_to_string(frame_rgb)
        #if text : 
        #    print(text)
        # Iterate over all detected text boxes
        #for i in range(len(data['text'])):
        #    if int(data['conf'][i]) > 60:  # Confidence level for text detection can be adjusted.
        #        # Get the bounding box coordinates
        #        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
#
                # Draw the bounding box
 #               frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the image
        cv2.imshow('Text Detection', cv2.flip(frame, 1))
        print(original)
        # Break the loop if 'q' is pressed
        cv2.waitKey(1)

    else:
        break

# Release the VideoCapture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()


 


#test = (pytesseract.image_to_data(gray, lang=None, config='', nice=0) ) #get confidence level if required

#print(pytesseract.image_to_boxes(gray))

 


 

'''required = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

Final = ''

 

for c in original:

    for ch in required:

        if c==ch:

         Final = Final + c 

         break

 

print (test)
'''