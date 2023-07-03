import pyzbar.pyzbar as pyzbar
import cv2
import time

def start_qr(img):
    text = None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
         
    decoded = pyzbar.decode(gray)  # 흑백 이미지에서 QR 코드를 감지하고 해독.
    urls = []
    for d in decoded:
        barcode_data = d.data.decode("utf-8")  # 바코드 데이터 디코딩합니다.
        barcode_type = d.type  # 바코드의 유형검출.
        
        text = '%s (%s)' % (barcode_data, barcode_type)
        if barcode_data.startswith('http://') or barcode_data.startswith('https://'):
            urls.append(barcode_data)
    return urls
   
if __name__ == "__main__":
    from picamera2 import Picamera2
    import requests
    picam2 = Picamera2()
    previous_urls = set()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    time.sleep(2.0)
    while True:
        img = picam2.capture_array()
        
        urls = start_qr(img)
        for url in urls:
            if url.startswith('http://') or url.startswith('https://'):
                try:
                    # Make a GET request to the URL
                    response = requests.get(url)
                    # If the request was successful, print the data
                    if response.status_code == 200:
                        print(response.text)
                    previous_urls.add(url)
                except requests.exceptions.RequestException as e:
                    # If an error occurred while making the request, print the error
                    print(f'An error occurred: {e}')
                
        cv2.imshow('Image', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break   
    picam2.stop()
    cv2.destroyAllWindows() 