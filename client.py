import socket
import cv2
import pickle
import struct
import threading
# from marker import ScreenMarker
import time
# from tts import Speaker

class Communication:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 8485))
        self.camera = cv2.VideoCapture(0)
        self.userID = 'F'  # 서버 접속시 ID전송
        data = self.userID.encode()
        message = struct.pack("B", ord('A')) + struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)
        
    def send_qrcode(self,qrcode):
        data = qrcode.encode()
        message = struct.pack("B", ord('W')) + struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)        
        
    def send_frame(self,frame):
            data = pickle.dumps(frame)
            message = struct.pack("B", ord(self.userID)) + struct.pack("Q", len(data)) + data
            self.client_socket.sendall(message)

    def send_menu(self,menu):
        data = menu.encode() # 인식한 사물이름 텍스트 전송
        message = struct.pack("B", ord('E')) + struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)
    
    def send_payment(self,payment):
        data = payment.encode() # 인식한 사물이름 텍스트 전송
        message = struct.pack("B", ord('R')) + struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)        
        
    def get_data(self, complete_choose, complete_payment, qrcode_menu):
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
                complete_choose = message
            elif data_type == ord('K'):
                message = frame_data.decode()
                complete_payment = message
            elif data_type == ord('V'):  # Message
                message = pickle.loads(frame_data)
                qrcode_menu = message

    def __del__(self):
        data = self.userID.encode()  # 접속 종료시 ID전송
        message = struct.pack("B", ord('E')) + struct.pack("Q", len(data)) + data
        self.client_socket.sendall(message)


    #client.camera.release()
    #client.client_socket.close()
