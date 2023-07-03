from multiprocessing import Queue, Process
import time
import os
import cv2
import tensorflow as tf
import numpy as np

from module.marker import ScreenMarker
from module.data_server import SharedDate
from module.tts import Speaker
from module.yolo_chatgpt import ObjectDetectionAssistant


def tts_proc(tts_Q, stop_event):
    tts = Speaker("en")
    while not stop_event.is_set():
        try:
            if not tts_Q.empty():
                s = tts_Q.get()
                if isinstance(s, str) and s is not None:
                    tts.speak(s)
        except:
            continue


def virtual_screen_proc(img_queue, motion_Q, stop_event):

    mk = ScreenMarker(camera_matrix_file='camera_mtx.npy',
                      dist_coeffs_file='camera_dist.npy')
    sd = SharedDate()

    tts_Q = Queue()
    get_tts = Process(target=tts_proc, args=(tts_Q, stop_event))
    get_tts.start()

    while True:  # not stop_event.is_set():
        # resive data

        # 캠 화면
        img = img_queue.get()
        sd.get_queue(motion_Q)

        try:
            if sd.store_IP is None:
                sd.store_IP = mk.startQr(img)  # 가게 ip

                if sd.store_IP in sd.IP_set:
                    print(sd.store_IP)
                    tts_Q.put("well come")
                else:
                    sd.store_IP = None
        except ValueError as e:
            # tts_Q.put(f"{e}")
            print(f"{e}")
        except:
            sd.store_IP = None
        if sd.qr_flag:
            mk.marker_screen(img)
            sd.menu_selection(mk, tts_Q, img)
        elif sd.motion == "Victory" and sd.store_IP is not None and sd.should_execute():
            sd.send_qrcode("5")
            print(sd.store_IP)
            sd.get_data()
            time.sleep(2)
            tts_Q.put(f"here is {sd.store_name}")
            sd.qr_flag = True
            sd.motion = None

        sd.send_frame(img)

    print("Process finished")


def detectorMotion_proc(queue_input, queue_output, stop_event):
    model = tf.keras.models.load_model('hand_model.h5')
    flag = 0
    dic_prediction = {
        0: ("Hand", 1),
        1: ("Good", 2),
        2: ("Victory", 3),
        3: ("Pointer", 4)
    }
    while not stop_event.is_set():
        if not queue_input.empty():
            item = queue_input.get()

            prediction = model.predict(np.array(item).reshape(1, -1))
            # prediction = model.predict(item)
            for index, (output_string, compare_flag) in dic_prediction.items():
                if prediction[0][index] > 0.95 and flag != compare_flag:
                    queue_output.put(output_string)
                    flag = compare_flag
                    break
                elif prediction[0][index] > 0.95:
                    break

    print("Process finished")


def assistant_proc(img_Q):
    assistant = ObjectDetectionAssistant(
        "yolov3.weights", "yolov3.cfg", "coco.names", "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")
    image_dir = "captured_images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print("realy_assistant")

    # while not stop_event.is_set():
    obj_list = []
    image_count = 0
    # event.wait()
    while image_count < 3:
        if not img_Q.empty():
            frame = img_Q.get()

            object_list = assistant.detect_objects(frame)
            obj_list += object_list

            image_path = os.path.join(image_dir, f"image_{image_count}.jpg")
            cv2.imwrite(image_path, frame)

            image_count += 1
            print(image_count)

    print(obj_list)
    messages = assistant.infer_location(obj_list)
    # event.close()
    print("assistant_finished")
