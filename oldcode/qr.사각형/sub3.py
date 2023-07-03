from collections import deque  # 동적 버퍼 적용을 위한 deque 모듈
import numpy as np             # 행렬 조작을 위한 numpy 모듈
import argparse                # 커맨드 라인을 통해 인자 전달을 위한 argparse 모듈
import imutils                 # 디스플레이 조정을 위한 imutils 모듈
import cv2                     # 컴퓨터 비전을 위한 주요 라이브러리인 OpenCV 모듈
import pyautogui               # 커서 접근 및 제어를 위한 pyautogui 모듈
pyautogui.FAILSAFE = False     # 트랙패드 입력 재정의

parser = argparse.ArgumentParser()      # 커맨드 라인에서 인자를 받기 위한 객체 생성
parser.add_argument("-v", "--video", help="path to the (optional) video file")  # 웹캠 또는 비디오 파일 경로를 받는 인자
parser.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")  # 버퍼 크기를 받는 인자
args = vars(parser.parse_args())    # 받은 모든 인자들을 args 변수에 저장

Lower = (29, 86, 6)                 # 색상 범위 지정을 위한 HSV 형식의 하한값
Upper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])  # 버퍼 크기에 맞는 deque 생성


if not args.get("video", False):    # 비디오 피드
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

while True: # 카메라가 켜져 있는 동안 다음 코드를 반복 실행
    
    (grabbed, frame) = camera.read()  # 카메라로부터 프레임 읽기

    if args.get("video") and not grabbed:
        break

    frame = imutils.resize(frame, width=800)  # 프레임 크기 조정하여 출력

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # BGR 형식을 HSV 형식으로 변환

    mask = cv2.inRange(hsv, Lower, Upper)       # 색상 검출과 노이즈 필터링을 위한 마스크 생성
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow('mask', mask)
    
    con = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 윤곽 검출
    center = None
    x = 0
    y = 0
    x0 = 0
    y0 = 0
    
    if len(con) > 0:  # 검출된 윤곽이 하나 이상인 경우
        
        c = max(con, key=cv2.contourArea)   # 가장 큰 크기의 윤곽 및 최소 분배 반경 찾기
        ((x, y), radius) = cv2.minEnclosingCircle(c)  # 핵심 단계 -> 윤곽의 반경과 중심(x, y) 얻기
        M = cv2.moments(c)      # 분포의 중심점 계산
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   # 타입 변환

        if radius > 10:  # 반경이 10보다 큰 경우
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # 반경 그리기
            cv2.circle(frame, center, 5, (0, 0, 255), -1)  # 중심점 그리기

    pts.appendleft(center)  # 데이터를 deque에 추가

    # 추적된 점들을 순회하며
    for i in xrange(1, len(pts)):
        
        if pts[i - 1] is None or pts[i] is None:
            continue

        # 그 외에는 선의 두께를 계산하고 연결된 선 그리기
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # 화면 크기에 따른 커서 명령
    if(radius < 30):
        pyautogui.moveTo(1366-2*x, 2*y)  # 스케일링
    else:
        x0 = 1366-(2*x)  # 좌표 고정 (사용자가 클릭하려는 경계에 있음을 이해하기 위함)
        y0 = 2*y
    
    if(radius > 40):
        pyautogui.click(x0, y0)  # 클릭 함수
     
    cmd = str(radius)
    cv2.putText(frame, cmd, (0, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # 반경 표시
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # 'q' 키가 눌리면 루프 종료
    if key == ord("q"):
        break

# 카메라 정리 및 열린 창 닫기
camera.release()
cv2.destroyAllWindows()