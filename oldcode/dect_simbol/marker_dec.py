import cv2, PIL
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from cv2 import aruco

frame = cv2.imread("aruco_photo.jpg")

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

print(rejectedImgPoints[1])