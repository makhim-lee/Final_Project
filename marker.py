import cv2
import numpy as np


class ArucoMarker:
    def __init__(self, marker_length=100, dictionary=cv2.aruco.DICT_4X4_50, camera_matrix_file='camera_mtx.npy', dist_coeffs_file='camera_dist.npy'):
        self.marker_length = marker_length
        self.arucoDict = cv2.aruco.getPredefinedDictionary(dictionary)
        self.arucoParams = cv2.aruco.DetectorParameters()
        self.camera_matrix = np.load(camera_matrix_file)  # Camera matrix
        self.dist_coeffs = np.load(dist_coeffs_file)  # Distortion coefficients

        self.rvecs = None
        self.tvecs = None

    def detect_markers(self, img):
        return cv2.aruco.detectMarkers(img, self.arucoDict, parameters=self.arucoParams)

    def estimate_pose(self, corners):
        self.rvecs, self.tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, self.marker_length, self.camera_matrix, self.dist_coeffs)

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

    def draw_paper_border(self, img, center, size):
        self.top_left = (center[0] - size[0]//2, center[1])
        self.bottom_right = (center[0] + size[0]//2,
                             center[1] + (size[1]*2)//3)
        cv2.rectangle(img, self.top_left, self.bottom_right, (0, 255, 0), 2)

    def distance_to_cam(self,):
        if self.tvecs is None:
            return None
        distance = np.linalg.norm(self.tvecs)
        self.distance = int((distance + 100)/20)
        return self.distance

    def angles_marker(self, ):
        rotation_matrix, _ = cv2.Rodrigues(self.rvecs)
        euler_angles = self.rotationMatrixToEulerAngles(rotation_matrix)
        euler_angles_degrees = np.degrees(euler_angles)
        self.angle_marker = euler_angles_degrees[1]
        return rotation_matrix, euler_angles_degrees


class ScreenMarker(ArucoMarker):
    def __init__(self, marker_length=100, dictionary=cv2.aruco.DICT_4X4_50, camera_matrix_file='camera_mtx.npy', dist_coeffs_file='camera_dist.npy'):
        super().__init__(
            marker_length=marker_length,
            dictionary=dictionary,
            camera_matrix_file=camera_matrix_file,
            dist_coeffs_file=dist_coeffs_file)
        self.top_left = None
        self.bottom_right = None
        self.distance = None
        self.angle_marker = None

        self.focal_length = 1620
        self.paper_width_cm = 21.0
        self.paper_height_cm = 29.7

    def reset_var(self):
        self.top_left = None
        self.bottom_right = None
        self.distance = None
        self.angle_marker = None

    def marker_screen(self, img):
        self.reset_var()
        (corners, ids, rejected) = self.detect_markers(img)

        if len(corners) > 0:
            ids = ids.flatten()
            index = None
            index = np.where(ids == 1)[0]

            if index is not None:
                self.estimate_pose(corners[index[0]])

                distance = self.distance_to_cam()
                _, _ = self.angles_marker()

                corners = corners[index[0]].reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)

                paper_width_px = int(
                    (self.focal_length * self.paper_width_cm) / distance)
                paper_height_px = int(
                    (self.focal_length * self.paper_height_cm) / distance)

                self.draw_paper_border(
                    img, (cX, cY), (paper_width_px, paper_height_px))

    def get_border_point(self):
        return self.top_left, self.bottom_right

    def get_screen_angle(self):
        text = None
        if self.angle_marker:
            if self.angle_marker < -4:
                text = "turn right"
            elif self.angle_marker > 4:
                text = "turn left"
        return text

    def XYtoButton(self, button_ratio):  # use numpy Broadcating
        scr_x_len = self.bottom_right[0] - self.top_left[0]
        scr_y_len = self.bottom_right[1] - self.top_left[1]
        button = button_ratio * \
            np.array([[scr_x_len, scr_y_len, scr_x_len, scr_y_len,]])
        button = button // 100
        button = button + \
            np.array([[self.top_left[0], self.top_left[1],
                     self.top_left[0], self.top_left[1],]])

        return button


if __name__ == '__main__':
    from picamera2 import Picamera2
    import time
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    time.sleep(2.0)
    marker = ScreenMarker(camera_matrix_file='camera_mtx.npy',
                          dist_coeffs_file='camera_dist.npy')
    while True:
        img = picam2.capture_array()
        marker.marker_screen(img)
        # distance = marker.distance_to_cam()
        # _, angle = marker.angles_marker()
        top_left, bottom_right = marker.get_border_point()
        if marker.top_left is not None and marker.bottom_right is not None:
            print(top_left, bottom_right)
            text = f"Distance: {marker.distance}, Angle: {marker.angle_marker}"
            cv2.putText(img, text, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Image', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
