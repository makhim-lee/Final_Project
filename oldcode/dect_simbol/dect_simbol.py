import cv2
import numpy as np

# 템플릿 이미지 로드
template_image = cv2.imread('template_image.png', cv2.IMREAD_GRAYSCALE)
# ORB 객체 생성
orb = cv2.ORB_create()
# 템플릿 이미지에 대해 키포인트와 디스크립터 계산
kp2, des2 = orb.detectAndCompute(template_image, None)
# BFMatcher 객체 생성
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

cap = cv2.VideoCapture(-1)

while True:
    # 비디오의 한 프레임씩 읽기
    ret, frame = cap.read()

    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 프레임에서 키포인트와 디스크립터 계산
    kp1, des1 = orb.detectAndCompute(gray_frame, None)

    # Matcher를 이용해 매칭 수행
    matches = bf.match(des1, des2)

    # 매칭 결과를 거리에 따라 정렬
    matches = sorted(matches, key=lambda x: x.distance)

    # 처음 10개 매칭만 그리기
    result_frame = cv2.drawMatches(gray_frame, kp1, template_image, kp2, matches[:10], None, flags=2)

    # 결과 출력
    cv2.imshow('Feature Matching', result_frame)

    # 'q' 키를 누르면 루프에서 빠져나오기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
