import socket
import cv2
import pickle
import struct
import threading
import numpy as np
import pandas as pd
import time

answer = 1   # input 쓰레드 입력값
MODE = 0    # 서버컴퓨터 화면 모드
userList = []   # 서버에 접속한 유저리스트
userLock = threading.Lock() # 쓰레드 Lock
qrcode = 0  # 인식한 qr코드 받아오는 변수
menu_statement = 0  # 현재 연결된 유저클라이언트가 인식한 메뉴창 상태

class Communication:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('169.254.217.121', 9999))
        self.server_socket.listen()

    def handle_client(self, conn):
        global answer
        global MODE
        global userList
        global qrcode
        global menu_statement
        data = b""
        payload_size = struct.calcsize("Q")
        

        while True:
            while len(data) < payload_size + 1:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            if not packet:
                break

            data_type, packed_msg_size = data[0], data[1:payload_size+1]
            data = data[payload_size+1:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            if data_type == ord('A'):  # 유저클라이언트 접속 시 ID 추가
                message = frame_data.decode()
                with userLock:
                    userList.append(message)
                    

            elif data_type == ord('W'):  # 유저클라이언트의 QR코드 인식 정보 확인
                message = frame_data.decode()
                qrcode = int(message)
                menu_statement = 1
                print(qrcode)
                
            elif data_type == ord('H'):  # 메뉴선택 혹은 결제화면 송신
                message = frame_data.decode()
                if message == "Stake":
                    menu_statement = 2
                elif message == "Shake":
                    menu_statement = 3
                elif message == "finish":
                    menu_statement = 4
                    
                print(message)
                
            elif MODE == 3 and data_type == ord(userList[int(answer)-1]) :  # 유저클라이언트의 프레임 스트리밍
                frame = pickle.loads(frame_data)
                cv2.imshow("Receiving Video", frame)
                key = cv2.waitKey(1) & 0xFF
                if answer == '0':
                    cv2.destroyAllWindows()
                    continue                                                  
        conn.close()
        
    def send_text(self,conn):
        global menu_statement
        global qrcode
        button1 = np.array([[23, 20, 77, 40], [23, 55, 77, 75]]) # 인식한 QRCODE의 좌표
        button2 = np.array([[3, 4, 6, 1]])
        coordinate = {
        'name': ['restaurant', 'hope'],
        'button_list': [['Stake', 'Shake'], ['soju']],
        'button_np': [button1, button2]
        }
        serialized_data = pickle.dumps(coordinate)
        while True:
            time.sleep(0.3)
            if qrcode == 5:           
                message = struct.pack("B", ord('V')) + struct.pack("Q", len(serialized_data)) + serialized_data # Qrcode 읽은 후 좌표데이터 전송
                conn.sendall(message)
                data = "2".encode()
                message = struct.pack("B", ord('J')) + struct.pack("Q", len(data)) + data # Qrcode를 읽었다는 신호 키오스크클라이언트에 전송
                conn.sendall(message)         
                break
        while True:
            time.sleep(0.3)
            if menu_statement == 2:
                data = "3".encode()
                message = struct.pack("B", ord('J')) + struct.pack("Q", len(data)) + data # 스테이크를 선택했다는 신호 키오스크클라이언트에 전송
                conn.sendall(message)
            elif menu_statement == 3:
                data = "4".encode()
                message = struct.pack("B", ord('J')) + struct.pack("Q", len(data)) + data # 쉐이크를 선택했다는 신호 키오스크클라이언트에 전송
                conn.sendall(message)  
            elif menu_statement == 4:
                data = "5".encode()
                message = struct.pack("B", ord('J')) + struct.pack("Q", len(data)) + data # 결제 완료 신호 키오스크클라이언트에 전송
                conn.sendall(message)  

    def run(self):
        global qrcode
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.send_text, args=(conn,)).start()
            threading.Thread(target=self.handle_client, args=(conn,)).start()

class Administrator:
    def get_userList(self):
        with userLock:
            for i in range(len(userList)):    
                print(str(i+1)+". user"+str(userList[i]))
            print("##### 처음화면 돌아가기 : 0 #####")

    def show_startMenu(self):
        print("####################################")
        print("1. 사용자 확인")
        print("2. 사용자 영상 출력")
        print("####################################")

    def show_display(self):
        global answer
        global MODE
        while True:
            if MODE == 0:
                self.show_startMenu()
                while True:
                    answer = input()
                    if answer == '1':  # 사용자 확인 메뉴
                        MODE = 1
                        break
                    elif answer == '2':  # 사용자 영상 출력 메뉴
                        MODE = 2
                        break
            elif MODE == 1:
                self.get_userList()
                while True:
                    answer = input()
                    if answer == '0':  
                        MODE = 0
                        break
            elif MODE == 2:
                self.get_userList()
                while True:
                    answer = input()
                    if answer == '0':  
                        MODE = 0
                        break
                    #elif userList[int(answer)]:
                    elif int(answer) <= len(userList):
                        MODE = 3
                        break
            elif MODE == 3:
                while True:
                    print("##### 처음화면 돌아가기 : 0 #####") # 메뉴화면 초기화
                    answer = input()
                    if answer == '0':
                        MODE = 0
                        break

admin = Administrator()
comm = Communication()


t = threading.Thread(target=admin.show_display)
t1 = threading.Thread(target=comm.run)

t.start()
t1.start()

t.join()
t1.join()
