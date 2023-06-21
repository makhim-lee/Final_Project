import pyzbar.pyzbar as pyzbar
import cv2
import time

def start_qr(img):
    text = None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
         
    decoded = pyzbar.decode(gray)  # 흑백 이미지에서 QR 코드를 감지하고 해독.
    for d in decoded:
        barcode_data = d.data.decode("utf-8")  # 바코드 데이터 디코딩합니다.
        barcode_type = d.type  # 바코드의 유형검출.
        
        text = '%s (%s)' % (barcode_data, barcode_type)

    return text
   
if __name__ == "__main__":
    print("import pyzbar, cv2")