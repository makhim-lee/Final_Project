import cv2
import mediapipe as mp
from picamera2 import Picamera2

#cap = cv2.VideoCapture(-1)
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()



mp_drawing = mp.solutions.drawing_utils # 손 위에 그림을 그릴 수 있는 메소드
mp_hands = mp.solutions.hands # MediaPipe solution에서 제공하는 손 모델

hands = mp_hands.Hands(
    max_num_hands = 1, # 인식할 손모양의 갯수, 생략하면 2가 지정된다.
    min_detection_confidence = 0.5, # 성공적인 것으로 간주되는 최소 신뢰도 값. 0.0 ~1.0사이로서 기본값은 0.5이다.
    min_tracking_confidence = 0.5) # 손 랜드마크가 성공적으로 추적된 것으로 간주되는 최소 신뢰도 값. 0.0 ~1.0 사이로서 기본값은 0.5이다. 이 값을 높이면 시간이 더 소요되지만 좀 더 정확한 작동이 보장된다. 
 
while True:
	img = picam2.capture_array()
	
	# OpenCV 영상은 BGR 형식인데 MediaPipe에서는 RGB 형식을 사용하므로 영상형식을 변환해 준다.
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	# MediaPipe의 hands 모듈을 이용해서 손동작을 인식한다. 손동작 인식 AI모델이 작동되고 결과 값이 result로 저장된다. 
	results = hands.process(imgRGB)
	# MediaPipe용 RGB 형식으로 변환했던 것을 OpenCV 영상처리를 위해 다시 BGR형식으로 되돌린다. 
	#imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

	# result값이 정상인 경우에만 후속 작업 처리한다. 
	if results.multi_hand_landmarks:
		# 실제 손이 인식될 때 점(랜드마크)을 찍는다.
		for handLms in results.multi_hand_landmarks:
			# results로 반환된 landmark 데이터를 사용한다. 인식된 손가락 모양은 index값을 가지는 배열로 제공된다.
			for id, lm in enumerate(handLms.landmark):
				h, w, c = img.shape
				cx, cy = int(lm.x*w), int(lm.y*h)
				print(id, " :" , cx, cy)
				if id == 0:
					cv2.circle(img, (cx,cy), 20, (255,0,0), cv2.FILLED)
					
        	# MediaPipe에 내장된 유틸리티 기능을 이용해서 구해진 손가락 모양을 서로 연결한 그림을 그려준다.
			mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

	cv2.imshow("Gotcha", img)
	cv2.waitKey(1)
