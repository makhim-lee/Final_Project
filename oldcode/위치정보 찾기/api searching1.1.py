import cv2
import numpy as np
import openai

# Yolo 로드
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# 이미지 가져오기
img = cv2.imread("sample.jpg")
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

# 정보를 화면에 표시
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # 좌표
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
obj_list = []
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        obj_list.append(label)

openai.api_key = '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'  # OpenAI API 키를 입력하세요

def infer_location(object_list):
    messages = [{"role": "system", "content": "You are an intelligent assistant."}]

    user_input = f"Please guess three representative places where these items are located {object_list}"

    messages.append({"role": "user", "content": user_input})

    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message

    print("Assistant:", reply["content"])

    messages.append(reply)

# 사용자가 입력한 사물 리스트
object_list = ""
for obj in obj_list:
    object_list = object_list + ", "+ f"{obj}"

infer_location(object_list)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()