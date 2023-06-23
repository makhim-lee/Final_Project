import pandas as pd
import cv2
import numpy as np
import detector as detec
from pprint import pprint
import time
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

detector = detec.HandDetector()
filename = "test.csv"
#filename = "landmarks.csv"
save_datas=[]
count = 0
while True:
    img = picam2.capture_array()
    detector.findHands(img)
    save_data = detector.findLandmarks(img)
    
    save_data = np.array([save_data])
    if cv2.waitKey(1) & 0xFF == ord('p'):#(lm_list is not None):
        if count == 0 :
            save_datas = save_data
            print(save_datas.shape)
        else :
            print(save_data.shape)
            save_datas = np.vstack((save_datas, save_data))
        #save_datas.append(save_data)
        count += 1
        time.sleep(1)
        print(count)
    cv2.imshow("Gotcha", cv2.flip(img, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pd_data = pd.DataFrame(save_datas)
        pd_data.to_csv(filename, mode='w')
        break


cv2.destroyAllWindows()

dateset = pd.read_csv(filename, index_col=0)
data = dateset.to_numpy()
pprint(data)

""" test append data
double_lists = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]

for _ in range(5):
    save_datas.append(double_lists)
    
pd_data = pd.DataFrame(save_datas)
pd_data.to_csv(filename, mode='w')# a ->덮어쓰기 x 추가 ㅇ

dateset = pd.read_csv(filename, index_col=0)
data = dateset.to_numpy()
pprint(data)
print(type(data)) 
"""
