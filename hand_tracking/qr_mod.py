import pyzbar.pyzbar as pyzbar
import cv2
def screen_qr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
         
    decoded = pyzbar.decode(gray)  # 흑백 이미지에서 QR 코드를 감지하고 해독.
    for d in decoded:
        x, y, w, h = d.rect  # 바코드의 위치와 크기를 가져옴.

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 검출된 바코드 주위에 사각형.
        cv2.rectangle(img, (x, y), (x + w*3, y+ h*3), (0,255,255),2)

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
    print(pyzbar.__version__)