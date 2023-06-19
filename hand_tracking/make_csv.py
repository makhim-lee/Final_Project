import pandas as pd
import cv2
import numpy as np
from detector import HandDetector
from pprint import pprint
import time

cap = cv2.VideoCapture(-1)
detector = HandDetector()
filename = "test.csv"
#filename = "landmarks.csv"
save_datas=[]
count = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lm_list,save_data = detector.findLandmarks(img)
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

cap.release()
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
