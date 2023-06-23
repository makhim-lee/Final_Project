import cv2
from marker import ScreenMarker
import time
from tts import Speaker

import numpy as np
import pandas as pd
import threading

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

    def make_DB(self,):
        button1 = np.array([[23, 20, 77, 40], [23, 60, 77, 80]])
        button2 = np.array([[3, 4, 6, 1]])

        data = {
            'name': ['restaurant', 'hope',],
            'button_list': [['Steak', 'Shake', ], ['soju',]],
            'button_np': [button1, button2]
        }
        IP = [5, 6]
        self.DB = pd.DataFrame(data, index=IP)

    def output_DB(self ):
        self.store_name, self.menu_name, self.button = self.DB.loc[self.store_IP]
        print(self.store_name, self.menu_name, self.button)
        


class SharedDate(Menu, Debouncer):
    def __init__(self,):
        Menu.__init__(self)
        Debouncer.__init__(self)
        
        self.motion = None
        self.pointer = None
        self.chose_menu = None
        self.finish_flag = False
        self.menu_flag = False
        self.qr_flag = False

# 손 좌표랑 모션 받아오는 thread
    def get_queue(self, motion_Q):
        
        if not motion_Q.empty():
            output = motion_Q.get()
            if isinstance(output, str) :
                self.motion = output
                print(self.motion)
            elif isinstance(output, list):
                self.pointer = output
        

    # 키오스크 이용
    def menu_selection(self, mk, tts,img):
        # 키오스크 화면 찾기
        try:
            if mk.top_left is None or mk.bottom_right is None:
                raise ValueError("No detecting screen")

            within_x_boundaries = mk.top_left[0] < self.pointer[0] < mk.bottom_right[0]
            within_y_boundaries = mk.top_left[1] < self.pointer[1] < mk.bottom_right[1]
            if not (within_x_boundaries and within_y_boundaries):
                raise ValueError("Pointer not within boundary")
            else:
                if self.button is not None:
                    for idx, val in enumerate(self.button):
                        val = mk.XYtoButton(val)
                        if len(val) > 0:
                            val = val[0]
                        cv2.rectangle(img, (val[0], val[1]), (val[2], val[3]), (0, 255, 0), 2)
                        if (val[0] < self.pointer[0] < val[2]) and (val[1] < self.pointer[1] < val[3]):
                            if not self.finish_flag and len(self.menu_name) > idx:                    
                                self.chose_menu = self.menu_name[idx]
                #               tts.speak(f"do you what {menu_name}")    
                            else :
                                self.chose_menu = "finish"
                                pass
                            cv2.putText(img, self.chose_menu, (50, 50), cv2.FONT_ITALIC, 1, (255,0,0), 2)
                        else :
                            self.chose_menu = None
                    if self.chose_menu == "finish" and self.motion == "far" and self.should_execute():
                        print("finish")
                        self.finish_flag = False
                        self.store_IP = None
                        self.menu_flag = False
                        self.chose_menu = None  
                    elif self.chose_menu is not None and self.motion == "far" and self.should_execute():   
                        self.button = self.finish_button
                        self.finish_flag = True
                        self.motion = None
                        self.qr_flag = False
                        print("ok")
                        
                        

                        
        except ValueError as e:
            #tts.speak(f"{e}")
            print(f"{e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # handle other unexpected errors


def mark_detec(img_queue, motion_Q, stop_event):
    cv2.namedWindow("img")
    # 키오스크 화면 찾아 주는 class
    mk = ScreenMarker(camera_matrix_file='camera_mtx.npy',
                      dist_coeffs_file='camera_dist.npy')
    qr_flag = False
    sd = SharedDate()
    sd.make_DB()
    click_int = Debouncer()

    tts = Speaker()
    #get_Q = threading.Thread(target=sd.get_queue, args=(motion_Q, stop_event))
    #get_Q.start()

    while True:
        # 캠 화면
        img = img_queue.get()
        sd.get_queue(motion_Q)

        # qr로 부터 가계 Ip 읽기 // qr 인식후엔 키오스크 화면 찾기
        try:
            if sd.store_IP is None:

                sd.store_IP = mk.startQr(img)  # 가게 ip

                if sd.store_IP is not None:
                    sd.output_DB()
        except:
            sd.store_IP = None
                    #tts.speak(f"here is {sd.store_name}")

    
        if sd.qr_flag:
            #screen_angle = mk.get_screen_angle()
            #if screen_angle is not None:
            #    tts.speak(screen_angle)
            mk.marker_screen(img)
            sd.menu_selection(mk, tts, img)
            
        elif sd.motion == "far" and sd.store_IP is not None and click_int.should_execute(): 
            sd.qr_flag = True
            sd.motion = None
        
        cv2.imshow("img", cv2.flip(img, 1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    cv2.destroyAllWindows()
    time.sleep(1)
    print("Process finished")


if __name__ == '__main__':
    pass
