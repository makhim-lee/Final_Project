import cv2
from marker import ScreenMarker
import time
from tts import tts_thread

import numpy as np
import pandas as pd
from threading import Thread
from queue import Queue
from multiprocessing import Process, Queue
class Debouncer:
    def __init__(self):
        self.delay = 2
        self.last_exec = 0
        
    def should_execute(self):
        now = time.time()
        if now - self.last_exec > self.delay:
            self.last_exec = now
            return True
        return False
      

class Menu:
    def __init__(self,):
        self.store_IP = None
        self.button = None
        self.menu_name = None
        self.store_name = None
        self.finish_button = np.array([[23, 60, 77, 80]])
        self.DB = None
        self.IP_set = None

    def make_DB(self,):
        button1 = np.array([[23, 20, 77, 40], [23, 60, 77, 80]])
        button2 = np.array([[3, 4, 6, 1]])

        data = {
            'name': ['restaurant', 'hope',],
            'button_list': [['Steak', 'Shake', ], ['soju',]],
            'button_np': [button1, button2]
        }
        IP = [5, 6]
        self.IP_set = set(IP)
        self.DB = pd.DataFrame(data, index=IP)

    def output_DB(self ):
        try:
            self.store_name, self.menu_name, self.button = self.DB.loc[self.store_IP]
            print(self.store_name, self.menu_name, self.button)
        except:
            print("no data")


class SharedDate(Menu, Debouncer):
    def __init__(self,):
        Menu.__init__(self)
        Debouncer.__init__(self)
        
        self.motion = None
        self.pointer = None
        self.chose_menu = None
        self.finish_flag = False
        #self.menu_flag = False
        self.qr_flag = False

# 손 좌표랑 모션 받아오는 thread
    def get_queue(self, motion_Q):
      
        if not motion_Q.empty():
            output = motion_Q.get()
            if isinstance(output, str) :
                self.motion = output
            elif isinstance(output, list):
                self.pointer = output
            
            
    # 키오스크 이용
    def menu_selection(self, mk, tts_Q,img):
        # 키오스크 화면 찾기
        try:
            if mk.top_left is None or mk.bottom_right is None:
                raise ValueError("")
                #No detecting screen
            within_x_boundaries = mk.top_left[0] < self.pointer[0] < mk.bottom_right[0]
            within_y_boundaries = mk.top_left[1] < self.pointer[1] < mk.bottom_right[1]
            if not (within_x_boundaries and within_y_boundaries):
                raise ValueError("not within boundary")
            else:
                if self.button is not None and self.pointer is not None:
                    button = mk.XYtoButton(self.button)
                    for idx, val in enumerate(button):
                        if np.isscalar(val):
                            continue  # Skip this iteration of the loop
                        else:
                            cv2.rectangle(img, (val[0], val[1]), (val[2], val[3]), (0, 255, 0), 2)
                            if (val[0] < self.pointer[0] < val[2]) and (val[1] < self.pointer[1] < val[3]):
                                if not self.finish_flag and len(self.menu_name) > idx:                    
                                    self.chose_menu = self.menu_name[idx]
                                    if tts_Q.empty() :
                                        tts_Q.put(f"{self.chose_menu}?")    
                                else :
                                    self.chose_menu = "finish"
                                    if tts_Q.empty() :
                                        tts_Q.put("calculate?")    
                                cv2.putText(img, self.chose_menu, (50, 50), cv2.FONT_ITALIC, 1, (255,0,0), 2)
                            else :
                                self.chose_menu = None
                                if tts_Q.empty(): 
                                    tts_Q.put("not chose")    
                  
                    print(self.motion)
                    if self.chose_menu is not None and self.motion == "far" and self.should_execute():   
                        if self.chose_menu == "finish":
                            self.finish_flag = False
                            self.store_IP = None
                            self.motion = None
                            tts_Q.put("Thank you")
                            time.sleep(2)
                        self.button = self.finish_button
                        self.finish_flag = True
                        self.motion = None
                        
                        tts_Q.put(f"you chose {self.chose_menu}") 
                        print("ok")          
                        
        except ValueError as e:
            if tts_Q.empty() :
                tts_Q.put(f"{e}")
            print(f"{e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # handle other unexpected errors


def mark_detec(img_queue, motion_Q, stop_event):
    cv2.namedWindow("img")
    # 키오스크 화면 찾아 주는 class
    mk = ScreenMarker(camera_matrix_file='camera_mtx.npy',
                      dist_coeffs_file='camera_dist.npy')
    sd = SharedDate()
    sd.make_DB()

    tts_Q = Queue() 
    get_tts = Process(target=tts_thread, args=(tts_Q, stop_event))
    get_tts.start()

    while True:
        # 캠 화면
       
        img = img_queue.get()
        sd.get_queue(motion_Q)

        # qr로 부터 가계 Ip 읽기 // qr 인식후엔 키오스크 화면 찾기
        try:
            
            if sd.store_IP is None:
                sd.store_IP, distance = mk.startQr(img)  # 가게 ip
                
                if sd.store_IP in sd.IP_set:
                    sd.output_DB()
                    print(sd.store_name)
                    tts_Q.put(f"here is {sd.store_name}")
        except ValueError as e:
            #tts.speak(f"{e}")
            print(f"{e}")
        
        except:
            sd.store_IP = None
                    #tts.speak(f"here is {sd.store_name}")

    
        if sd.qr_flag:
            
            mk.marker_screen(img)
            sd.menu_selection(mk, tts_Q, img)
            
        elif sd.motion == "far" and sd.store_IP is not None and sd.should_execute(): 
            sd.qr_flag = True
            sd.motion = None
            tts_Q.put(f"next page")
            time.sleep(2)
        
        #cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    cv2.destroyAllWindows()
    print("Process finished")

if __name__ == '__main__':
    pass
