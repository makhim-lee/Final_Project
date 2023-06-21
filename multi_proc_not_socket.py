import cv2
from marker import ScreenMarker
import time
from tts import Speaker
from qr_mod import start_qr
import numpy as np
import pandas as pd
import threading


class Menu:
    def __init__(self,):
        self.store_IP = None
        self.button = None
        self.menu_name = None
        self.store_name = None
        self.finish_button = None
        self.DB = None

    def make_DB(self,):
        button1 = np.array([[17, 26, 83, 62], [17, 57, 83, 73]])
        button2 = np.array([[3, 4, 6, 1]])

        data = {
            'name': ['restaurant', 'hope',],
            'button_list': [['Steak', 'Shake', ], ['soju',]],
            'button_np': [button1, button2]
        }
        IP = [101, 102]
        self.DB = pd.DataFrame(data, index=IP)

    def output_DB(self, mk):
        self.store_name, self.menu_name, self.button = self.DB.loc[self.store_IP]
        self.finish_button = mk.XYtoButton(np.array([[17, 75, 83, 92]]))
        self.button = mk.XYtoButton(self.button)


class SharedDate(Menu):
    def __init__(self,):
        self.motion = None
        self.pointer = None

        self.menu_flag = False

# 손 좌표랑 모션 받아오는 thread
    def get_queue(self, motion_Q, stop_event):
        while not stop_event.is_set():
            if not motion_Q.empty():
                output = motion_Q.get()
                print(type(output))

                if type(output) == "string":
                    self.motion = output
                elif type(output) == "list":
                    self.pointer = output

    # 키오스크 이용
    def menu_selection(self, mk, tts):
        # 키오스크 화면 찾기
        try:
            if self.motion != "pointer":
                raise ValueError("No hand in camera")
            if mk.top_left is None or mk.bottom_right is None:
                raise ValueError("No detecting screen")

            within_x_boundaries = mk.top_left[0] < self.pointer[0] < mk.bottom_right[0]
            within_y_boundaries = mk.top_left[1] < self.pointer[1] < mk.bottom_right[1]
            if not (within_x_boundaries and within_y_boundaries):
                raise ValueError("Pointer not within boundary")
            else:
                if self.button is not None:
                    for idx, val in enumerate(self.button):
                        if (val[0] < self.pointer[0] < val[3]) and (val[1] < self.pointer[1] < val[4]):
                            menu_name = self.menu[idx]
                            tts.speak(f"do you what {menu_name}")
                            self.menu_flag = True
                            break
                        else:
                            raise ValueError("nothing choose menu")
                    if self.menu_flag and self.motion == "Victory":
                        # 메뉴 선택시 서버에 보낼 메세지
                        self.send_mess(f"{menu_name}")
                else:
                    raise ValueError("No button")
            if self.finish_flag is not None:
                tts.speak("finish choose menu")
                self.finish_flag = None
                self.store_IP = None

        except ValueError as e:
            tts.speak(f"{e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # handle other unexpected errors


def mark_detec(img_queue, motion_Q, stop_event):
    cv2.namedWindow("img")
    # 키오스크 화면 찾아 주는 class
    mk = ScreenMarker(camera_matrix_file='camera_mtx.npy',
                      dist_coeffs_file='camera_dist.npy')
    # thread 간 데이터 공유하는 class
    sd = SharedDate()
    sd.make_DB()

    # tts 언어 지정
    tts = Speaker()
    get_Q = threading.Thread(target=sd.get_queue, args=(motion_Q, stop_event))
    get_Q.start()

    while True:
        # 캠 화면
        img = img_queue.get()

        # qr로 부터 가계 Ip 읽기 // qr 인식후엔 키오스크 화면 찾기
        if sd.store_IP is None:
            sd.store_IP = start_qr(img)  # 가게 ip

            if sd.store_IP is not None:
                sd.output_DB()
                time.sleep(1)
                tts.speak(f"here is {sd.store_name}")
        else:
            screen_angle = mk.get_screen_angle()
            if screen_angle is not None:
                tts.speak(screen_angle)
            mk.marker_screen(img)
            sd.menu_selection(mk, tts)

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
