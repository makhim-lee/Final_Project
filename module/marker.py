import cv2
import numpy as np
import time


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
        self.distance = int((distance + 100)/40)
        return self.distance

    def angles_marker(self, ):
        rotation_matrix, _ = cv2.Rodrigues(self.rvecs)
        euler_angles = self.rotationMatrixToEulerAngles(rotation_matrix)
        euler_angles_degrees = np.degrees(euler_angles)
        self.angle_marker = euler_angles_degrees[1]


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
        
        self.last_exec = None
        self.angle_list = []

    def reset_var(self):
        self.top_left = None
        self.bottom_right = None
        self.distance = None
        self.angle_marker = None
        self.cX = None
        self.cY = None

    def marker_screen(self, img):
        self.reset_var()
        (corners, ids, rejected) = self.detect_markers(img)

        if len(corners) > 0 and len(ids) > 0:
            ids = ids.flatten()
            #index = None
            #index = np.where(ids == 1)[0]

            if ids[0] == 1:
                self.estimate_pose(corners[0])

                distance = self.distance_to_cam()

                corners = corners[0].reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                self.cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                self.cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(img, (self.cX, self.cY), 4, (0, 0, 255), -1)

                paper_width_px = int(
                    (self.focal_length * self.paper_width_cm) / (2 * distance))
                paper_height_px = int(
                    (self.focal_length * self.paper_height_cm) / (2 * distance))

                self.draw_paper_border(
                    img, (self.cX, self.cY), (paper_width_px, paper_height_px))
                

    def get_border_point(self):
        return self.top_left, self.bottom_right

    def get_screen_angle(self):
        text = None
        now = time.time()
        if self.last_exec == None : 
            self.last_exec = now
        elif now - self.last_exec < 3 and self.angle_marker is not None:
            self.angle_list.append(self.angle_marker)
        elif now - self.last_exec > 3 and self.angle_list:
            if len(self.angle_list) > 0 :
                average = sum(self.angle_list) / len(self.angle_list)

                if average > 25:
                    text = "turn right"
                elif average < -8:
                    text = "turn left"
                self.angle_list = []
                self.last_exec = None
        return text
    
    def find_region(self, point):   
        if isinstance(self.bottom_right, tuple) and isinstance(self.top_left, tuple):
            # Assuming square_size is the length of the side of the square
            region_size_x = (self.bottom_right[0] - self.top_left[0]) / 3
            region_size_y = (self.bottom_right[1] - self.top_left[1]) / 3

            # Calculate the boundaries of the square
            left_boundary = self.cX - (self.bottom_right[0] - self.top_left[0])  / 2
            top_boundary = self.cY - (self.bottom_right[1] - self.top_left[1]) / 2

            # Calculate relative position of the point within the square
            relative_x = point[0] - left_boundary
            relative_y = point[1] - top_boundary

            # Calculate region index (0-8)
            region_x = int(relative_x // region_size_x)
            region_y = int(relative_y // region_size_y)

            # Convert to 2D grid index (0, 0) to (2, 2)
            grid_index = (region_y, region_x)
        else:
            grid_index = None

        return grid_index

    def XYtoButton(self, button_ratio):  # use numpy Broadcating
        button = None
        try:
            scr_x_len = self.bottom_right[0] - self.top_left[0]
            scr_y_len = self.bottom_right[1] - self.top_left[1]
            button = button_ratio * np.array([[scr_x_len, scr_y_len, scr_x_len, scr_y_len,]])
            button = button // 100
            button = button + \
                np.array([[self.top_left[0], self.top_left[1],
                         self.top_left[0], self.top_left[1],]])
        except:
            pass
        return button
    
    def startQr(self,img):
        ids = None
        _, ids, _ = self.detect_markers(img)
        if ids is not None:
            ids = ids[0][0]
        return ids
'''
        ids = None
        self.reset_var()
        (corners, ids, rejected) = self.detect_markers(img)

        if len(corners) > 0 and len(ids) > 0:
            ids = ids.flatten()
            #index = None
            #index = np.where(ids == 1)[0]

            if ids[0] == 5:
                self.estimate_pose(corners[0])

                distance = self.distance_to_cam()
                self.angles_marker()
                corners = corners[0].reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
                ids = ids[0]
               
          
        return ids, distance
'''

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
    
    aaa = np.array([[23, 60, 77, 80]])
    while True:
        img = picam2.capture_array()
        marker.marker_screen(img)
        AAA = marker.find_region([500,500])
        print(AAA)
        #ids = marker.startQr(img)
        #print(ids)
        #angle = marker.get_screen_angle()
        #if angle is not None :
        #    print(angle)
        #print(marker.distance_to_cam())
        
        # distance = marker.distance_to_cam()
        # _, angle = marker.angles_marker()
        #top_left, bottom_right = marker.get_border_point()
        #if marker.top_left is not None and marker.bottom_right is not None:
        #    
        #    test = marker.get_screen_angle()
        #    print(test)
        #
        #    text = f"Distance: {marker.distance}, Angle: {marker.angle_marker}"
        #    cv2.putText(img, text, (50, 50),
        #                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            #button = marker.XYtoButton(aaa)
            #if button is not None:
            #    for idx, val in enumerate(button):
            #        if np.isscalar(val):
            #            continue  # Skip this iteration of the loop
            #        else:
            #            cv2.rectangle(img, (val[0], val[1]), (val[2], val[3]), (0, 255, 0), 2)
        cv2.imshow('Image', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
