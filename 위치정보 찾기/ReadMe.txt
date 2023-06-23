Api 활용 입력 정보 기반 위치 유추/ chat gpt활용 

Api 입력<---- 필수


sudo pip3 install openai  / 설치필수

실행파일 nano +로 파일제작



6.12qr코드 검출 수정

6.13 qr코드 서버 체크

6.14 네모 꼭지점검출 업데이트 메모리 부족현상 해결

6.14 프레임 안정화를 위한 중간값 필터링으로 흔들림 수정

다크넷 설치 및 필요파일 리눅스 환경 설치

필요설치 코드

pip install opencv-python (메인 오픈cv 필요 파이썬 인식코드)

pip install pyzbar(qr코드 인식 관련 필요코드)

pip install requests(http등 서버 연결에 용이 tcp/ip방식이 아닌 서버연결)

pip install numpy(넘파이코드)

sudo pip3 install openai / 설치필수

git clone https://github.com/pjreddie/darknet <---- 그대로 복붙

cd darknet

make

wget https://pjreddie.com/media/files/yolov3.weights <---- 그대로 복붙

파이썬 실행 // 코드 안에 인식되는 것<---sample.jpg 카메라 송출로 교체
Api 활용 입력 정보 기반 위치 유추/ chat gpt활용

Api 입력<---- 필수

++++ api searching. 1.1 업데이트 Yolo + Guess기능 추가 화면에 검출된 객체 기반 장소 유추 가능 // 질문 변경을 통해서 변형 답변가능

++++ 1.2 업데이트 class 형식으로 수정// 가중치 모델 변경 확인

+++ 1.3 업데이트 카메라 연동 / 카메라에 연동된 객체 탐지 후 탐지된 객체를 바탕으로 api를 활용해 위치 유추기능추가(미완)
