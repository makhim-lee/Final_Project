import pyzbar.pyzbar as pyzbar
import cv2
import requests

cap = cv2.VideoCapture(0)  # 객체를 생성.

i = 0
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

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 검출된 바코드 주위에 사각형.

        text = '%s (%s)' % (barcode_data, barcode_type)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)  # 바코드 데이터와 유형을 텍스트로 표시.

        # 서버로 데이터 보내기
        data = {'barcode_data': barcode_data, 'barcode_type': barcode_type}
        response = requests.post('http://127.0.0.1:9999', data=data)  # 데이터를 서버로 전송합니다.
        if response.status_code == 200:
            print('데이터가 성공적으로 전송되었습니다.')
        else:
            print('데이터 전송에 실패했습니다.')

    cv2.imshow('img', img)  # 이미지를 화면에 표시합니다.

    key = cv2.waitKey(1)  # 키 입력을 대기합니다.
    if key == ord('q'):  # 'q' 키를 누르면 루프를 종료합니다.
        break
    elif key == ord('s'):  # 's' 키를 누르면 이미지를 'qr.jpg'로 저장합니다.
        i += 1
        cv2.imwrite('qr.jpg', img)

cap.release()  
cv2.destroyAllWindows() 