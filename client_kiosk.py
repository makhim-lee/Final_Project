import socket
import threading
import time
import matplotlib.pyplot as plt
import struct
import matplotlib.image as mpimg
import pygame as pg
from tkinter import Tk, Canvas
from PIL import ImageTk
import requests
import threading
import time

# 서버 정보
SERVER_HOST = '169.254.217.121'
SERVER_PORT = 9999
# 변수 초기값
image_path = 'welcome.jpg'
stop_flag = False

class Communication:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))
        
    def get_data(self):
        global image_path
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

            if data_type == ord('J'):  # 서버에서 보내준 신호로 상황에 맞게 키오스크 화면 변경 
                message = int(frame_data.decode())
                print(message)

                if message == 2:
                    image_path = 'choose_menu.jpg'
                elif message == 3:
                    image_path = 'pay_stake.jpg'
                elif message == 4:
                    image_path = 'pay_shake.jpg'
                elif message == 5:
                    image_path = 'complete.jpg'
            
    def __del__(self):
        self.client_socket.close()
        # 소켓 연결 종료

def show_image():
    global image_path
    fig = None
    x = 1 
    while True:
        # 이미지 열기
        img = mpimg.imread(image_path)

        if fig is None:
            # 최초 실행 시에만 창 생성
            dpi = 70
            height, width, _ = img.shape
            figsize = (width / float(dpi), height / float(dpi))
            fig = plt.figure(figsize=figsize, dpi=dpi)
            
            plt.imshow(img)
            plt.axis('off')  # 축 제거
            plt.tight_layout()  # 레이아웃 조정
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # 이미지를 가운데 정렬

        else:
            # 이미지 업데이트
            plt.imshow(img)
            fig.canvas.draw()

        plt.pause(0.1)  # 이미지 표시 갱신 주기 (0.1초)
        
        if x == 1: # 원활한 
            x = input()

com = Communication()
t = threading.Thread(target=com.get_data) # 서버에서 보내는 데이터를 받는 쓰레드
t2 = threading.Thread(target=show_image) # 키오스크 화면 동작 쓰레드

t.start()
t2.start()

t.join()
t2.join()
