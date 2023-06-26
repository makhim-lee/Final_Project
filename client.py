import socket
import cv2
import pickle
import struct
import threading

import time

import numpy as np
import pandas as pd
import threading

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
        IP = [1, 2]
        self.DB = pd.DataFrame(data, index=IP)

    def output_DB(self ):
        self.store_name, self.menu_name, self.button = self.DB.loc[self.store_IP]

class Communication:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 9999))
        self.camera = cv2.VideoCapture(0)

        self.userID = 'F'  # 서버 접속시 ID전송
        data = self.userID.encode()
        message = struct.pack("B", ord('A')) + struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)
        
    def send_frame(self):
        while self.camera.isOpened():
            ret, frame = self.camera.read()
            data = pickle.dumps(frame)
            message = struct.pack("B", ord(self.userID)) + struct.pack("Q", len(data)) + data
            self.client_socket.sendall(message)
            
    def send_text(self):
        text = input()  # 인식한 사물이름 텍스트 전송
        data = text.encode()
        message = struct.pack("B", ord('W')) + struct.pack("Q", len(data)) + data
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

            if data_type == ord('N'):  # Message
                message = frame_data.decode()
                print("text " + message)
            elif data_type == ord('V'):  # Message
                message = pickle.loads(frame_data)
                print(message)

    def __del__(self):
        data = self.userID.encode()  # 접속 종료시 ID전송
        message = struct.pack("B", ord('E')) + struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)

client = Communication()

t = threading.Thread(target=client.send_frame)
t1 = threading.Thread(target=client.send_text)
t2 = threading.Thread(target=client.get_data)

t.start()
t1.start()
t2.start()

t.join()
t1.join()
t2.join()

client.camera.release()
client.client_socket.close()
