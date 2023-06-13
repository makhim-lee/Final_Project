import pyzbar.pyzbar as pyzbar
import cv2
import requests

cap = cv2.VideoCapture(0)  # 객체를 생성.

i = 0
text = ""
while(cap.isOpened()):
    ret, img = cap.read()  #  프레임을 읽기.

    if not ret:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
         
    decoded = pyzbar.decode(gray)  # 흑백 이미지에서 QR 코드를 감지하고 해독.

    for d in decoded: 
        x, y, w, h = d.rect  # 바코드의 위치와 크기를 가져옴.

        barcode_data = d.data.decode("utf-8")  # 바코드 데이터 디코딩합니다.
        barcode_type = d.type  # 바코드의 유형검출.
        
        text = '%s (%s)' % (barcode_data, barcode_type)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 검출된 바코드 주위에 사각형.
        print(x,y, w,h)
        cv2.rectangle(img, (x, y), (x + w*3, y+ h*3), (0,255,255),2)

    cv2.imshow("img", cv2.flip(img, 1))
    if text:
        print(text)
    key = cv2.waitKey(1)  # 키 입력을 대기합니다.
    if key == ord('q'):  # 'q' 키를 누르면 루프를 종료합니다.
        break
    elif key == ord('s'):  # 's' 키를 누르면 이미지를 'qr.jpg'로 저장합니다.
        i += 1
        cv2.imwrite('qr.jpg', img)

cap.release()  
cv2.destroyAllWindows() 