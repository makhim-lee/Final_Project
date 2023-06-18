
#!https://chev.me/arucogen/

import cv2
import numpy as np

# load the ArUCo dictionary and grab the ArUCo parameters
class marker() :
    def __init__(self,) :
        self.marker_length = 100
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.arucoParams = cv2.aruco.DetectorParameters()
        
        self.camera_matrix = np.load('camera_mtx.npy')  # Camera matrix
        self.dist_coeffs = np.load('camera_dist.npy')  # Distortion coefficients
        
    def marker_dec(self, img) :
        (corners, ids, rejected) = cv2.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)
        if len(corners) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
                
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
                
                cv2.putText(img, str(markerID),(topLeft[0], topLeft[1] - 15),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
    
    def marker_screen(self, img):
        (corners, ids, rejected) = cv2.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)
        
        if len(corners) > 0 :
            ids = ids.flatten()
        value_to_find = 1
        index = np.where(ids == value_to_find)[0][0]
        if index.size > 0:
		##distance
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners[index], self.marker_length, self.camera_matrix, self.dist_coeffs)
            distance = np.linalg.norm(tvecs)
            
            (topLeft, topRight, bottomRight, bottomLeft) = corners[index]
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
            cv2.putText(img, str(value_to_find)+"and"+str(distance),(topLeft[0], topLeft[1] - 15),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
            cv2.rectangle(img, pt1, pt2, (0,0,225), thickness=2)        

		


