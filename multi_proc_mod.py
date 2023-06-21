import cv2
from marker import ScreenMarker
import time
from tts import speak
from qr_mod import start_qr 

import threading

class SharedDate :
    def __init(self):

        
        self.motion = None
        self.pointer = None
        self.store_IP = None

## 손 좌표랑 모션 받아오는 thread
def get_queue(shared_data,motion_Q, stop_event):
    while not stop_event.is_set():
        if not motion_Q.empty():
            output = motion_Q.get()
            print(type(output))

            if type(output) == "string":
                shared_data.motion = output
            elif type(output) == "list":
                shared_data.pointer = output

## 키오스크 이용 프로세스 thread
def calculation (mk, sd):
    while sd.store_IP is not None:
        ## 키오스크 화면 찾기
        if not(mk.top_left is None and mk.bottom_right is None) and sd.motion == "pointer":
            within_x_boundaries = mk.top_left[0] < sd.pointer[0] < mk.bottom_right[0]
            within_y_boundaries = mk.top_left[1] < sd.pointer[1] < mk.bottom_right[1]
            if within_x_boundaries and within_y_boundaries:
                speak("in noundar")
        
        ## 서버에서 받아온 버튼 위치 찾기 
                
    
        sd.store_IP = None

def mark_detec(img_queue, motion_Q, stop_event):
    cv2.namedWindow("img")
    ## 키오스크 화면 찾아 주는 class
    mk = ScreenMarker(camera_matrix_file='camera_mtx.npy',
                          dist_coeffs_file='camera_dist.npy')
    ## thread 간 데이터 공유하는 class 
    sd = SharedDate()
    
    get_Q = threading.Thread(target=get_queue, args=(sd, motion_Q, stop_event))
    calcuation_thread = threading.Thread(target=calculation, args=(mk, sd))
    
    get_Q.start()
    
    while True:  
        ## 캠 화면 
        img = img_queue.get()
       
        ##qr로 부터 가계 Ip 읽기 // qr 인식후엔 키오스크 화면 찾기 
        if sd.store_IP is None:
            sd.store_IP = start_qr(img) ## 가게 ip 
        else :
            mk.marker_screen(img) 
            
        
        if sd.store_IP is not None and not calcuation_thread.is_alive() :
            store_name = "coffe"## 서버에서 받고 싶음 힘들면 고정값도 ㄱㅊ
            speak(f"here is {store_name}")
            calcuation_thread.start()
  
  
        cv2.imshow("img", cv2.flip(img, 1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
    cv2.destroyAllWindows()
    
    time.sleep(1)
    calcuation_thread.jion()
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