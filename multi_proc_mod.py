import cv2
from marker import ScreenMarker
import time
from tts import Speaker
from qr_mod import start_qr 

import threading
## 여기다 만들어주셈 완성되면 딴파일로 움길겨

import socket
class Socket:
    def __init__(self, IP="1270.0.0.1", Port="9999"):
        host = socket.gethostname() 
        port = Port 

        client_socket = socket.socket()
        client_socket.connect((host, port))
    def send_mess():
        ## 가게 ip
        ## 버튼 클릭 신호 
        pass
    def receive_mess():
        ##가게이름 
        ##키오스크 페이지number
        ##버튼 좌표
        ## xy 고정 좌표가 아니라 전체 화면의 몇퍼센트의 위치 이런식으로 값을 받고싶음
        ## 결제완료 
        pass
    
    

class SharedDate :
    def __init__(self):

        self.motion = None
        self.pointer = None
        self.store_IP = None

## 손 좌표랑 모션 받아오는 thread
    def get_queue(self,motion_Q, stop_event):
        while not stop_event.is_set():
            if not motion_Q.empty():
                output = motion_Q.get()
                print(type(output))

                if type(output) == "string":
                    self.motion = output
                elif type(output) == "list":
                    self.pointer = output

    ## 키오스크 이용
    def calculation (self, mk, tts):
        ## 키오스크 화면 찾기
        try:
            if self.motion != "pointer":
                raise ValueError("No hand in camera")
            if mk.top_left is None or mk.bottom_right is None:
                raise ValueError("No detecting screen")

            within_x_boundaries = mk.top_left[0] < self.pointer[0] < mk.bottom_right[0]
            within_y_boundaries = mk.top_left[1] < self.pointer[1] < mk.bottom_right[1]
            if not (within_x_boundaries and within_y_boundaries):
                raise ValueError("Pointer not within boundary")

        except ValueError as e:
            tts.speak(f"{e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # handle other unexpected errors

        

    ## 서버에서 받아온 버튼 위치 찾기 
            
    
        self.store_IP = None

def mark_detec(img_queue, motion_Q, stop_event):
    cv2.namedWindow("img")
    ## 키오스크 화면 찾아 주는 class
    mk = ScreenMarker(camera_matrix_file='camera_mtx.npy',
                          dist_coeffs_file='camera_dist.npy')
    ## thread 간 데이터 공유하는 class 
    sd = SharedDate()
    ## tts 언어 지정
    tts = Speaker()
    get_Q = threading.Thread(target=sd.get_queue, args=(motion_Q, stop_event))
    get_Q.start()
    
    while True:  
        ## 캠 화면 
        img = img_queue.get()
       
        ##qr로 부터 가계 Ip 읽기 // qr 인식후엔 키오스크 화면 찾기 
        if sd.store_IP is None:
            sd.store_IP = start_qr(img) ## 가게 ip 
            if sd.store_IP is not None :
                store_name = "coffe"## 서버에서 받고 싶음 힘들면 고정값도 ㄱㅊ
                tts.speak(f"here is {store_name}")
        else :
            mk.marker_screen(img)
            sd.calculation(mk, tts) 
 
  
        cv2.imshow("img", cv2.flip(img, 1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
        
        
    cv2.destroyAllWindows()
    time.sleep(1)
    get_Q.join()
    print("Process finished")


if __name__ == '__main__':
    pass


    #if not motion_Q.empty():
    #    output = motion_Q.get()
    #    print(type(output))
    #  
    #    if type(output) == "string":
    #        motion = output
    #    elif type(output) == "list":
    #        pointer = output