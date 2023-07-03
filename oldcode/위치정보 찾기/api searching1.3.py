import cv2
import numpy as np
import openai
import time

class ObjectDetectionAssistant:
    def __init__(self, weights_file, config_file, names_file, api_key):
        self.net = cv2.dnn.readNet(weights_file, config_file)
        self.classes = []
        with open(names_file, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.api_key = api_key

    def detect_objects(self, frame):
        img = cv2.resize(frame, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:  # Adjust the confidence threshold as needed
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
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
                label = str(self.classes[class_ids[i]])
                color = self.colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
                obj_list.append(label)

        return obj_list, img

    def infer_location(self, object_list):
        openai.api_key = self.api_key

        messages = [{"role": "system", "content": "You are an intelligent assistant."}]
        user_input = f"Please guess three representative places where these items are located: {object_list}"
        messages.append({"role": "user", "content": user_input})

        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message

        print("Assistant:", reply["content"])
        messages.append(reply)

        return messages


# Usage example:
assistant = ObjectDetectionAssistant("yolov4.weights", "yolov4.cfg", "coco.names", "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")
cap = cv2.VideoCapture(0)  # Change 0 to the appropriate camera index if using multiple cameras

last_detection_time = 0
detection_interval = 10  # in seconds

obj_set = set()
while True:
    current_time = time.time()
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection every `detection_interval` seconds
    object_list, image = assistant.detect_objects(frame)
    obj_set.update(object_list)  # Use `update` to add elements to the set

    cv2.imshow("Frame", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if len(obj_set) >= 10:  # Break the loop when the set contains 10 unique objects
        break

messages = assistant.infer_location(obj_set)
cap.release()
cv2.destroyAllWindows()