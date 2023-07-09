import cv2
import time

import numpy as np
import pandas as pd

import socket
import pickle
import struct


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

        # 데이터베이스

        self.store_IP = None
        self.button = None
        self.menu_name = None
        self.store_name = None
        self.DB = None
        self.check_page = None
        self.IP_set = set([5, 6])
        self.finish_button = np.array([[23, 60, 77, 80]])

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

        self.menu_flag = False
        self.qr_flag = None
        self.finish_flag = False
# 손 좌표랑 모션 받아오는 thread

    def get_queue(self, motion_Q):

        if not motion_Q.empty():
            output = motion_Q.get()
            if isinstance(output, str):
                self.motion = output
            elif isinstance(output, list):
                self.pointer = output
                self.motion = None
            print(self.motion)

    def menu_selection(self, mk, tts_Q, img):
        # 키오스크 화면 찾기
        try:
            if mk.top_left is None or mk.bottom_right is None:
                raise ValueError("")
                # No detecting screen
            within_x_boundaries = mk.top_left[0] < self.pointer[0] < mk.bottom_right[0]
            within_y_boundaries = mk.top_left[1] < self.pointer[1] < mk.bottom_right[1]
            chosen_menu_exists = False
            if not (within_x_boundaries and within_y_boundaries):
                raise ValueError("not within boundary")
            else:
                if self.button is not None and self.pointer is not None:
                    button = mk.XYtoButton(self.button)
                    for idx, val in enumerate(button):
                        if np.isscalar(val):
                            continue  # Skip this iteration of the loop
                        else:
                            cv2.rectangle(
                                img, (val[0], val[1]), (val[2], val[3]), (0, 255, 0), 2)
                            if (val[0] < self.pointer[0] < val[2]) and (val[1] < self.pointer[1] < val[3]):
                                if not self.finish_flag and len(self.menu_name) > idx:
                                    self.chose_menu = self.menu_name[idx]
                                    chosen_menu_exists = True
                                    cv2.putText(
                                        img, self.chose_menu, (50, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
                                    if tts_Q.empty():
                                        tts_Q.put(f"{self.chose_menu}?")
                                elif self.finish_flag:
                                    self.chose_menu = "finish"
                                    chosen_menu_exists = True
                                    if tts_Q.empty():
                                        tts_Q.put("calculate?")

                            else:
                                if chosen_menu_exists:
                                    chosen_menu_exists = False
                                else:
                                    self.chose_menu = None
                                    if tts_Q.empty():
                                        tts_Q.put("not chose")

                    print(self.motion)
                    if self.chose_menu is not None and self.motion == "Victory":
                        if self.chose_menu == "finish":
                            self.send_menu(self.chose_menu)
                            self.finish_flag = False
                            self.store_IP = None
                            self.motion = None
                            self.qr_flag = False
                            tts_Q.put("Thank you")
                        else:
                            self.button = self.finish_button
                            self.finish_flag = True
                            self.motion = None
                            print(self.chose_menu)
                            self.send_menu(self.chose_menu)
                            tts_Q.put(f"you chose {self.chose_menu}")
                            print("ok")
        except ValueError as e:
            if tts_Q.empty():
                tts_Q.put(f"{e}")
            print(f"{e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # handle other unexpected errors


if __name__ == '__main__':

    pass
