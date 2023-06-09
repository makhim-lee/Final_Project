import cv2
import time

import numpy as np
import pandas as pd

import socket
import pickle
import struct
import logging

logging.basicConfig(level=logging.INFO)

## Prevent double click
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

##socket
class Communication:
    def __init__(self):
        # 서버 설정
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('169.254.217.121', 9999))
        self.userID = 'F'  # 서버 접속시 ID전송
        data = self.userID.encode()
        message = struct.pack("B", ord('A')) + \
            struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)
        # database
        self.store_IP = None
        self.button = None
        self.menu_name = None
        self.store_name = None
        self.DB = None
        self.check_page = None
        self.IP_set = set([5, 6])
        self.finish_button = np.array([[23, 60, 77, 80]])
        self.finish_menu = ['finish']

# 가게식별
    def send_qrcode(self, qrcode):

        data = qrcode.encode()
        print(type(self.store_IP))
        message = struct.pack("B", ord('W')) + \
            struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)

# 스트리밍
    def send_frame(self, frame):
        data = pickle.dumps(frame)
        message = struct.pack("B", ord(self.userID)) + \
            struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)

    def send_menu(self, menu):
        data = menu.encode()  # 인식한 사물이름 텍스트 전송
        message = struct.pack("B", ord('H')) + \
            struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)

    def get_data(self):
        data = b""
        payload_size = struct.calcsize("Q")

        while True:
            while len(data) < payload_size + 1:
                packet = self.client_socket.recv(4096)
                if not packet:
                    break
                data += packet

            if not packet:
                break

            data_type, packed_msg_size = data[0], data[1:payload_size+1]
            data = data[payload_size+1:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += self.client_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            if data_type == ord('V'):  # Message
                message = pickle.loads(frame_data)
                print(message)
                IP = [5, 6]
                self.DB = pd.DataFrame(message, index=IP)
                self.store_name, self.menu_name, self.button = self.DB.loc[self.store_IP]
                print(self.store_name, self.menu_name, self.button)
                break


class SharedDate(Communication, Debouncer):
    def __init__(self):
        Communication.__init__(self)
        Debouncer.__init__(self)

        self.motion = None
        self.pointer = None
        self.store_IP = None

        self.qr_flag = None
## 손 좌표랑 모션 받아오는 thread
    def get_queue(self, motion_Q):

        if not motion_Q.empty():
            output = motion_Q.get()
            if isinstance(output, str):
                self.motion = output
            elif isinstance(output, list):
                self.pointer = output
                self.motion = None
            print(self.motion)
    
    def draw_rectangle_and_check_boundaries(self, val):
        cv2.rectangle(img, (val[0], val[1]), (val[2], val[3]), (0, 255, 0), 2)
        return val[0] < self.pointer[0] < val[2] and val[1] < self.pointer[1] < val[3]
## 가상디스플레이 상호작용
    def menu_selection(self, marker, tts_Q, img):    
        try:
            if marker.top_left is None or marker.bottom_right is None:
                raise ValueError("Invalid corner values")

            within_x_boundaries = marker.top_left[0] < self.pointer[0] < marker.bottom_right[0]
            within_y_boundaries = marker.top_left[1] < self.pointer[1] < marker.bottom_right[1]
            if not (within_x_boundaries and within_y_boundaries):
                raise ValueError("Not within boundary")

            if self.pointer is None:
                raise ValueError("No pointer detected")

            if self.button is None:
                raise ValueError("No data button")

            button = marker.XYtoButton(self.button)
## 버튼 생성및 손좌표 대조
            for idx, val in enumerate(button):
                if np.isscalar(val):
                    continue
                within_button_boundaries = self.draw_rectangle_and_check_boundaries(val)
                if within_button_boundaries:    
                    if len(self.menu_name) > idx:
                        self.chose_menu = self.menu_name[idx]
                        cv2.putText(img, self.chose_menu, (50, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
                        if tts_Q.empty():
                            tts_Q.put(f"{self.chose_menu}?")
## 선택 이밴트 발생 조건 
            if self.chose_menu is not None and self.motion == "Victory":
                self.motion = None
                self.send_menu(self.chose_menu)

                if self.chose_menu == "finish":
                    self.store_IP = None
                    self.qr_flag = False
                    tts_Q.put("Thank you")
                else:
                    self.menu_name = self.finish_menu
                    self.button = self.finish_button
                    tts_Q.put(f"You chose {self.chose_menu}")

                self.chose_menu = None
            elif tts_Q.empty():
                tts_Q.put("Not chosen")

        except ValueError as e:
            if tts_Q.empty():
                tts_Q.put(f"{e}")
            logging.error(f"ValueError: {e}")

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        
        
        
        
        
if __name__ == '__main__':

    pass
