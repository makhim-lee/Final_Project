
#!https://chev.me/arucogen/

import cv2
import numpy as np

# load the ArUCo dictionary and grab the ArUCo parameters


class Marker():
    def __init__(self,):
        self.marker_length = 100
        self.arucoDict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50)
        self.arucoParams = cv2.aruco.DetectorParameters()

        self.camera_matrix = np.load('camera_mtx.npy')  # Camera matrix
        # Distortion coefficients
        self.dist_coeffs = np.load('camera_dist.npy')

        self.top_left = None
        self.bottom_right = None
        self.distanc_to_mark = None
        self.screen_rotation_angle = None

    def marker_screen(self, img):
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            img, self.arucoDict, parameters=self.arucoParams)
        self.top_left = None
        self.bottom_right = None
        self.distanc_to_mark = None
        self.screen_rotation_angle = None
        if len(corners) > 0:
            ids = ids.flatten()
            value_to_find = 1
            index = np.where(ids == value_to_find)[0][0]

            if index >= 0:
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners[index], self.marker_length, self.camera_matrix, self.dist_coeffs)
                distance = np.linalg.norm(tvecs)
                distance = int((distance + 100)/20)
                self.distanc_to_mark = (distance)
                rotation_matrix, _ = cv2.Rodrigues(rvecs)
                euler_angles = self.rotationMatrixToEulerAngles(
                    rotation_matrix)
                euler_angles_degrees = np.degrees(euler_angles)
                self.screen_rotation_angle = (euler_angles_degrees[1])

                corners = corners[index].reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
                if distance > 0:
                    text_posi = f"distance : {distance}"
                    cv2.putText(img, text_posi, (int(topLeft[0]), int(
                        topLeft[1] - 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

                    focal_length = 1620
                    paper_width_cm = 21.0
                    paper_height_cm = 29.7

                    paper_width_px = int(
                        (focal_length * paper_width_cm) / distance)
                    paper_height_px = int(
                        (focal_length * paper_height_cm) / distance)

                    self.draw_paper_border(
                        img, (cX, cY), (paper_width_px, paper_height_px))

    def draw_paper_border(self, img, center, size):
        self.top_left = (center[0] - size[0]//2, center[1])
        self.bottom_right = (center[0] + size[0]//2,
                             center[1] + (size[1]*2)//3)

        cv2.rectangle(img, self.top_left, self.bottom_right, (0, 255, 0), 2)


# Calculates Rotation Matrix given euler angles.


    def rotationMatrixToEulerAngles(self, R):
        sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        singular = sy < 1e-6
        if not singular:
            x = np.arctan2(R[2, 1], R[2, 2])
            y = np.arctan2(-R[2, 0], sy)
            z = np.arctan2(R[1, 0], R[0, 0])
        else:
            x = np.arctan2(-R[1, 2], R[1, 1])
            y = np.arctan2(-R[2, 0], sy)
            z = 0
        return np.array([x, y, z])


if __name__ == "__main__":
    print("test mod")
    from picamera2 import Picamera2
    import time
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    time.sleep(2.0)
    mark = Marker()
    while True:
        img = picam2.capture_array()
        # mark.marker_dec(img)
        mark.marker_screen(img)
        print(mark.top_left, mark.bottom_right,
              mark.distanc_to_mark, mark.screen_rotation_angle)
        cv2.imshow("IMG", cv2.flip(img, 1))
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
    cv2.destroyAllWindows()
