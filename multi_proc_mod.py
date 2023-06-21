import cv2
from marker import ScreenMarker
import time
from tts import Speaker
from qr_mod import start_qr
import numpy as mp
import threading


import socket


class Socket:
    def __init__(self, IP="1270.0.0.1", Port="9999"):
        self.host = socket.gethostname()
        self.port = Port

        self.client_socket = socket.socket()

        # socket 통신으로 업데이트 할 내용
        self.page_num = None
        self.button = None
        self.menu = None
        self.store_name = None
        self.finish_flag = None

    def connect_socket(self):
        self.client_socket.connect((self.host, self.port))

    def send_mess(self):
        # 가게 ip
        # 버튼 클릭 신호
        pass

    def receive_mess(self, mk, stop_event):
        while not stop_event.is_set():
            try:
                pass
            except:
                pass
        # 가게이름
        # 키오스크 페이지number
        # 버튼 좌표()
            # xy 고정 좌표가 전체화면중 [x1_ratio,y1_ratio,x2_ratio,y2_ratio] 이런식으로 받고 싶음
            # int 형 (0 ~ 100)
            # 2차원 numpy로 넘겨 줄것
            #  np.array([[0번 버튼],
            #            [1번 버튼],
            #            [2번 버튼],])
        # 메뉴명 list[0번 버튼 메뉴명:str, 1번 버튼 메뉴명:str ....]
        # 결제완료
            # 버튼 좌표를 계산해주는 코드(page_num)이 바뀔떄 실행되게 하면 될듯 ?
            self.button = mk.XYtoButton(self.button)


class SharedDate(Socket):
    def __init__(self, IP="1270.0.0.1", Port="9999"):
        super().__init__(IP=IP, Port=Port)

        self.motion = None
        self.pointer = None
        self.store_IP = None

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
    # thread 간 데이터 공유하는 class + run_socket
    sd = SharedDate(IP="1270.0.0.1", Port="9999")
    sd.connect_socket()
    rece_mess = threading.Thread(target=sd.receive_mess, args=(mk, stop_event))
    rece_mess.start()
    # tts 언어 지정
    tts = Speaker()
    get_Q = threading.Thread(target=sd.get_queue, args=(motion_Q, stop_event))
    get_Q.start()

    while True:
        # 캠 화면
        img = img_queue.get()
        # receive_socket
        sd.receive_mess()
        # qr로 부터 가계 Ip 읽기 // qr 인식후엔 키오스크 화면 찾기
        if sd.store_IP is None:
            sd.store_IP = start_qr(img)  # 가게 ip
            # send store_Ip
            sd.send_mess(sd.store_IP)

            if sd.store_IP is not None:
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
    rece_mess.join()
    print("Process finished")


if __name__ == '__main__':
    pass

    # if not motion_Q.empty():
    #    output = motion_Q.get()
    #    print(type(output))
    #
    #    if type(output) == "string":
    #        motion = output
    #    elif type(output) == "list":
    #        pointer = output
