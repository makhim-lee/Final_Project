import cv2
import numpy as np

# 카메라 열기
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 프레임을 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 케니 엣지 검출- 경계를 찾아주는 알고리즘 물체의 경계를 뚜렷하게함
    edges = cv2.Canny(gray, 50, 150)

    # 컨투어 검출 - 이미지에서 객체의 윤곽선을 찾아줌
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 왼쪽 위와 오른쪽 아래의 네모를 저장할 변수
    top_left = None
    bottom_right = None

    # 컨투어를 순회하며 네모 검출
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # 꼭지점의 개수가 4개인 경우에만 사각형으로 판단
        if len(approx) == 4:
            # 왼쪽 위와 오른쪽 아래의 꼭지점 저장
            points = approx.reshape(-1, 2)
            rect_top_left = np.min(points, axis=0)
            rect_bottom_right = np.max(points, axis=0)

            # 첫 번째 네모일 경우
            if top_left is None:
                top_left = rect_top_left
                bottom_right = rect_bottom_right
            else:
                # 두 번째 네모일 경우, 최솟값과 최댓값을 업데이트하여 전체적인 사각형 계산
                top_left = np.minimum(top_left, rect_top_left)
                bottom_right = np.maximum(bottom_right, rect_bottom_right)

    # 네모 그리기
    if top_left is not None and bottom_right is not None:
        cv2.rectangle(frame, tuple(top_left), tuple(bottom_right), (0, 255, 255), 2)

    # 화면에 출력
    cv2.imshow("Rectangle", frame)


# 카메라 해제
cap.release()
cv2.destroyAllWindows()