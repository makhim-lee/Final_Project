import numpy as np
import math
r = np.array([[-0.00809613,  0.89989849,  0.43602427],
            [ 0.99644167, -0.0293226,   0.0790201 ],
            [ 0.08389544,  0.43511251, -0.89645895]])


def eulerAnglesToRotationMatrix(theta) :
    R_x = np.array([[1,         0,                  0              ],
                    [0,         np.cos(theta[0]), -np.sin(theta[0]) ],
                    [0,         np.sin(theta[0]), np.cos(theta[0])  ]
                    ])
 
    R_y = np.array([[np.cos(theta[1]),    0,      np.sin(theta[1])  ],
                   [0,                     1,      0                   ],
                   [-np.sin(theta[1]),   0,      np.cos(theta[1])  ]
                   ])
 
    R_z = np.array([[np.cos(theta[2]),    -np.sin(theta[2]),    0],
                    [np.sin(theta[2]),    np.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])

    R = np.dot(R_z, np.dot( R_y, R_x ))
    
    return R
def rotationMatrixToEulerAngles(R):
    sy = np.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2,1], R[2,2])
        y = np.arctan2(-R[2,0], sy)
        z = np.arctan2(R[1,0], R[0,0])
    else:
        x = np.arctan2(-R[1,2], R[1,1])
        y = np.arctan2(-R[2,0], sy)
        z = 0
    return np.array([x, y, z])


#R = eulerAnglesToRotationMatrix(r)
#print(R)
R = rotationMatrixToEulerAngles(r)
print(R)