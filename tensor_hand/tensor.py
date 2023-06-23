import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib as plt

from sklearn.model_selection import train_test_split


print(tf.__version__)
# 데이터 불러오기
hand_motions_bak = [
[0.233, 0.879, 0.000, 0.297, 0.856, -0.035,0.332, 0.791, -0.052,0.291, 0.729, -0.069,0.245, 0.697, -0.084,0.338, 0.644, -0.020,0.381, 0.547, -0.044,0.407, 0.483, -0.058,0.426, 0.427, -0.068,0.285, 0.627, -0.023,0.302, 0.501, -0.047,0.310, 0.424, -0.062,0.316, 0.361, -0.072,0.239, 0.644, -0.031,0.229, 0.601, -0.060,0.235, 0.685, -0.060,0.243, 0.744, -0.051,0.198, 0.682, -0.045,0.197, 0.665, -0.070,0.210, 0.724, -0.072,0.222, 0.769, -0.066],
[0.251, 0.766, 0.000,0.303, 0.724, -0.047,0.316, 0.661, -0.071,0.258, 0.624, -0.090,0.211, 0.608, -0.107,0.297, 0.513, -0.044,0.319, 0.401, -0.071,0.332, 0.328, -0.086,0.339, 0.266, -0.098,0.241, 0.513, -0.040,0.225, 0.388, -0.069,0.208, 0.308, -0.086,0.194, 0.246, -0.099,0.201, 0.544, -0.040,0.162, 0.534, -0.073,0.183, 0.610, -0.079,0.208, 0.661, -0.073,0.171, 0.594, -0.047,0.146, 0.602, -0.075,0.167, 0.651, -0.083,0.195, 0.682, -0.081],
[0.310, 0.814, 0.000,0.365, 0.797, -0.033,0.397, 0.743, -0.050,0.362, 0.679, -0.065,0.327, 0.640, -0.079,0.423, 0.611, -0.024,0.474, 0.527, -0.046,0.505, 0.473, -0.059,0.529, 0.424, -0.068,0.376, 0.589, -0.025,0.405, 0.473, -0.048,0.418, 0.400, -0.061,0.429, 0.344, -0.070,0.334, 0.599, -0.032,0.323, 0.567, -0.058,0.322, 0.633, -0.057,0.324, 0.681, -0.049,0.293, 0.630, -0.044,0.285, 0.614, -0.066,0.292, 0.658, -0.069,0.302, 0.693, -0.064],
[0.313, 0.782, 0.000,0.361, 0.750, -0.027,0.390, 0.685, -0.034,0.368, 0.612, -0.041,0.338, 0.562, -0.047,0.405, 0.596, 0.001,0.442, 0.529, -0.011,0.464, 0.484, -0.019,0.482, 0.445, -0.025,0.365, 0.579, 0.001,0.379, 0.486, -0.011,0.389, 0.431, -0.022,0.398, 0.387, -0.028,0.328, 0.588, -0.004,0.329, 0.536, -0.023,0.332, 0.596, -0.022,0.332, 0.642, -0.016,0.295, 0.610, -0.015,0.301, 0.575, -0.032,0.306, 0.615, -0.034,0.307, 0.648, -0.029],
[0.222, 0.769, 0.000,0.265, 0.703, -0.015,0.277, 0.625, -0.015,0.248, 0.559, -0.018,0.211, 0.527, -0.021,0.267, 0.576, 0.028,0.287, 0.510, 0.023,0.298, 0.469, 0.019,0.304, 0.433, 0.015,0.229, 0.568, 0.022,0.216, 0.486, 0.016,0.212, 0.440, 0.008,0.207, 0.401, 0.002,0.196, 0.581, 0.008,0.185, 0.509, -0.004,0.207, 0.552, -0.004,0.218, 0.597, 0.000,0.166, 0.605, -0.009,0.164, 0.546, -0.020,0.180, 0.566, -0.019,0.189, 0.601, -0.015],
[0.237, 0.729, 0.000,0.289, 0.716, -0.064,0.311, 0.681, -0.104,0.263, 0.670, -0.134,0.220, 0.665, -0.162,0.290, 0.532, -0.094,0.309, 0.421, -0.133,0.316, 0.351, -0.152,0.318, 0.291, -0.166,0.229, 0.525, -0.083,0.207, 0.408, -0.125,0.191, 0.329, -0.144,0.178, 0.266, -0.158,0.184, 0.549, -0.077,0.176, 0.578, -0.113,0.204, 0.656, -0.118,0.225, 0.701, -0.115,0.153, 0.590, -0.078,0.151, 0.641, -0.103,0.180, 0.694, -0.112,0.208, 0.720, -0.114],
[0.458, 0.713, 0.000,0.510, 0.747, -0.070,0.553, 0.765, -0.132,0.546, 0.771, -0.188,0.520, 0.754, -0.240,0.572, 0.609, -0.134,0.628, 0.545, -0.197,0.665, 0.492, -0.234,0.698, 0.445, -0.261,0.524, 0.581, -0.134,0.535, 0.489, -0.210,0.546, 0.421, -0.241,0.560, 0.359, -0.260,0.475, 0.584, -0.136,0.485, 0.645, -0.195,0.494, 0.717, -0.199,0.509, 0.752, -0.194,0.434, 0.608, -0.147,0.449, 0.695, -0.184,0.463, 0.759, -0.189,0.481, 0.785, -0.189],
[0.339, 0.729, 0.000,0.375, 0.734, -0.043,0.412, 0.699, -0.059,0.415, 0.618, -0.071,0.419, 0.556, -0.080,0.487, 0.652, -0.025,0.553, 0.634, -0.041,0.597, 0.621, -0.052,0.634, 0.608, -0.060,0.468, 0.609, -0.017,0.533, 0.559, -0.035,0.571, 0.525, -0.050,0.603, 0.495, -0.060,0.438, 0.586, -0.015,0.446, 0.530, -0.039,0.417, 0.561, -0.045,0.398, 0.589, -0.042,0.402, 0.576, -0.018,0.408, 0.537, -0.040,0.392, 0.565, -0.047,0.384, 0.595, -0.045],
[0.332, 0.694, 0.000,0.351, 0.688, -0.059,0.381, 0.659, -0.081,0.395, 0.584, -0.095,0.415, 0.528, -0.105,0.473, 0.650, -0.045,0.540, 0.657, -0.064,0.586, 0.660, -0.075,0.625, 0.662, -0.085,0.466, 0.610, -0.028,0.540, 0.588, -0.050,0.583, 0.566, -0.070,0.619, 0.549, -0.085,0.445, 0.580, -0.017,0.455, 0.526, -0.048,0.417, 0.530, -0.064,0.394, 0.543, -0.067,0.418, 0.561, -0.012,0.421, 0.519, -0.040,0.391, 0.533, -0.053,0.373, 0.555, -0.057],
[0.492, 0.868, 0.000,0.510, 0.791, -0.017,0.506, 0.714, -0.046,0.492, 0.689, -0.082,0.469, 0.714, -0.117,0.395, 0.670, -0.037,0.340, 0.607, -0.075,0.303, 0.583, -0.098,0.268, 0.564, -0.116,0.374, 0.724, -0.059,0.290, 0.705, -0.105,0.235, 0.695, -0.128,0.186, 0.687, -0.142,0.376, 0.782, -0.083,0.373, 0.749, -0.124,0.432, 0.736, -0.123,0.474, 0.735, -0.117,0.397, 0.836, -0.111,0.417, 0.796, -0.138,0.463, 0.780, -0.137,0.496, 0.770, -0.132],
[0.517, 0.867, 0.000,0.552, 0.810, -0.018,0.554, 0.742, -0.036,0.519, 0.722, -0.057,0.484, 0.728, -0.078,0.480, 0.646, -0.018,0.455, 0.557, -0.043,0.435, 0.509, -0.058,0.414, 0.472, -0.069,0.444, 0.678, -0.031,0.381, 0.605, -0.058,0.342, 0.567, -0.072,0.308, 0.541, -0.080,0.425, 0.726, -0.048,0.406, 0.702, -0.076,0.450, 0.737, -0.074,0.479, 0.769, -0.066,0.419, 0.781, -0.069,0.422, 0.764, -0.090,0.461, 0.787, -0.089,0.489, 0.810, -0.083],
[0.502, 0.893, 0.000,0.541, 0.846, -0.029,0.549, 0.781, -0.044,0.508, 0.753, -0.060,0.468, 0.748, -0.076,0.499, 0.667, -0.019,0.489, 0.578, -0.040,0.480, 0.521, -0.054,0.469, 0.473, -0.065,0.456, 0.690, -0.023,0.410, 0.604, -0.048,0.378, 0.558, -0.061,0.352, 0.521, -0.069,0.432, 0.733, -0.032,0.409, 0.706, -0.062,0.443, 0.755, -0.062,0.468, 0.791, -0.054,0.418, 0.787, -0.046,0.409, 0.769, -0.072,0.437, 0.800, -0.074,0.461, 0.823, -0.068],
[0.436, 0.904, 0.000,0.340, 0.812, 0.060,0.320, 0.728, 0.091,0.341, 0.653, 0.115,0.367, 0.610, 0.145,0.289, 0.646, 0.060,0.222, 0.546, 0.087,0.185, 0.482, 0.112,0.153, 0.443, 0.129,0.347, 0.609, 0.037,0.305, 0.472, 0.067,0.289, 0.404, 0.095,0.273, 0.355, 0.112,0.409, 0.607, 0.018,0.401, 0.573, 0.057,0.401, 0.620, 0.084,0.397, 0.648, 0.099,0.470, 0.628, -0.000,0.450, 0.616, 0.031,0.447, 0.654, 0.047,0.444, 0.686, 0.059],
[0.433, 0.903, 0.000,0.376, 0.773, 0.067,0.385, 0.672, 0.056,0.426, 0.604, 0.037,0.458, 0.546, 0.021,0.341, 0.644, -0.081,0.312, 0.514, -0.127,0.281, 0.431, -0.154,0.256, 0.363, -0.169,0.391, 0.675, -0.112,0.403, 0.500, -0.168,0.415, 0.401, -0.171,0.421, 0.319, -0.170,0.444, 0.697, -0.126,0.483, 0.533, -0.117,0.487, 0.552, -0.042,0.482, 0.591, 0.003,0.500, 0.710, -0.136,0.518, 0.575, -0.100,0.509, 0.593, -0.037,0.497, 0.633, 0.006],
[0.456, 0.373, 0.000,0.519, 0.445, -0.020,0.541, 0.551, -0.033,0.531, 0.622, -0.034,0.517, 0.682, -0.031,0.491, 0.594, -0.089,0.509, 0.745, -0.115,0.519, 0.825, -0.126,0.525, 0.893, -0.134,0.431, 0.596, -0.072,0.402, 0.771, -0.100,0.380, 0.859, -0.107,0.357, 0.923, -0.114,0.397, 0.590, -0.048,0.414, 0.718, -0.048,0.455, 0.716, -0.027,0.476, 0.703, -0.016,0.378, 0.577, -0.026,0.404, 0.678, -0.018,0.434, 0.679, -0.004,0.456, 0.659, 0.007],
[0.397, 0.729, 0.000,0.450, 0.616, 0.089,0.510, 0.598, 0.126,0.562, 0.632, 0.153,0.590, 0.660, 0.185,0.562, 0.552, 0.060,0.639, 0.484, 0.084,0.684, 0.442, 0.096,0.719, 0.409, 0.097,0.592, 0.609, 0.030,0.695, 0.586, 0.046,0.768, 0.575, 0.048,0.824, 0.571, 0.042,0.600, 0.671, 0.014,0.620, 0.703, 0.062,0.581, 0.710, 0.086,0.558, 0.705, 0.091,0.595, 0.731, 0.002,0.604, 0.760, 0.047,0.571, 0.762, 0.065,0.549, 0.757, 0.073],
[0.344, 0.673, 0.000,0.352, 0.550, 0.054,0.385, 0.487, 0.078,0.443, 0.482, 0.093,0.481, 0.500, 0.113,0.433, 0.422, 0.042,0.472, 0.316, 0.055,0.504, 0.247, 0.071,0.522, 0.195, 0.080,0.481, 0.450, 0.017,0.564, 0.362, 0.028,0.623, 0.312, 0.043,0.664, 0.270, 0.052,0.515, 0.506, -0.004,0.543, 0.531, 0.020,0.518, 0.563, 0.039,0.494, 0.568, 0.051,0.534, 0.586, -0.024,0.549, 0.612, -0.004,0.522, 0.628, 0.007,0.494, 0.637, 0.015],
[0.380, 0.851, 0.000,0.330, 0.773, 0.038,0.325, 0.695, 0.050,0.357, 0.639, 0.054,0.389, 0.610, 0.062,0.304, 0.633, 0.036,0.273, 0.538, 0.037,0.252, 0.476, 0.042,0.235, 0.430, 0.046,0.340, 0.614, 0.012,0.338, 0.496, 0.015,0.337, 0.423, 0.024,0.336, 0.367, 0.029,0.382, 0.615, -0.011,0.411, 0.575, -0.000,0.415, 0.608, 0.017,0.409, 0.633, 0.029,0.428, 0.628, -0.035,0.445, 0.605, -0.024,0.443, 0.633, -0.015,0.434, 0.656, -0.006],
[0.337, 0.908, 0.000,0.312, 0.801, 0.045,0.336, 0.720, 0.058,0.388, 0.682, 0.061,0.431, 0.673, 0.067,0.339, 0.650, 0.041,0.349, 0.538, 0.040,0.354, 0.465, 0.043,0.357, 0.408, 0.046,0.379, 0.657, 0.011,0.430, 0.541, 0.012,0.462, 0.471, 0.019,0.484, 0.415, 0.024,0.418, 0.686, -0.017,0.464, 0.660, -0.008,0.454, 0.696, 0.011,0.439, 0.719, 0.025,0.456, 0.727, -0.045,0.481, 0.709, -0.036,0.468, 0.738, -0.024,0.450, 0.760, -0.014],
[0.189, 0.864, 0.000,0.175, 0.724, 0.071,0.217, 0.631, 0.098,0.285, 0.598, 0.109,0.336, 0.597, 0.126,0.232, 0.537, 0.068,0.271, 0.409, 0.076,0.292, 0.324, 0.086,0.303, 0.261, 0.093,0.279, 0.552, 0.029,0.369, 0.432, 0.038,0.421, 0.361, 0.053,0.455, 0.303, 0.061,0.321, 0.593, -0.007,0.399, 0.593, 0.011,0.381, 0.642, 0.034,0.356, 0.662, 0.050,0.361, 0.650, -0.042,0.410, 0.663, -0.025,0.389, 0.701, -0.011,0.360, 0.721, 0.000],
[0.259, 0.842, 0.000,0.331, 0.814, -0.018,0.396, 0.763, -0.029,0.444, 0.716, -0.045,0.455, 0.663, -0.059,0.347, 0.613, 0.003,0.405, 0.568, -0.022,0.437, 0.612, -0.036,0.452, 0.655, -0.043,0.316, 0.578, -0.013,0.340, 0.470, -0.031,0.374, 0.410, -0.048,0.402, 0.357, -0.063,0.279, 0.575, -0.036,0.280, 0.458, -0.057,0.298, 0.385, -0.071,0.319, 0.322, -0.083,0.244, 0.597, -0.064,0.224, 0.509, -0.084,0.221, 0.445, -0.095,0.227, 0.386, -0.103],
[0.326, 0.669, 0.000,0.391, 0.686, -0.024,0.459, 0.686, -0.037,0.514, 0.676, -0.052,0.548, 0.645, -0.066,0.472, 0.541, -0.009,0.539, 0.525, -0.033,0.553, 0.575, -0.046,0.552, 0.618, -0.052,0.456, 0.487, -0.019,0.520, 0.414, -0.037,0.569, 0.377, -0.054,0.609, 0.344, -0.070,0.424, 0.458, -0.037,0.466, 0.362, -0.056,0.500, 0.305, -0.072,0.533, 0.260, -0.084,0.384, 0.450, -0.058,0.398, 0.366, -0.078,0.414, 0.313, -0.088,0.435, 0.268, -0.096],
[0.372, 0.664, 0.000,0.428, 0.709, -0.037,0.482, 0.731, -0.069,0.515, 0.755, -0.100,0.544, 0.775, -0.130,0.526, 0.596, -0.076,0.585, 0.651, -0.129,0.579, 0.722, -0.155,0.561, 0.775, -0.170,0.506, 0.548, -0.090,0.579, 0.512, -0.144,0.639, 0.501, -0.180,0.695, 0.486, -0.208,0.466, 0.522, -0.109,0.518, 0.448, -0.160,0.565, 0.406, -0.194,0.612, 0.369, -0.217,0.416, 0.520, -0.130,0.432, 0.452, -0.171,0.448, 0.401, -0.194,0.471, 0.356, -0.211],
[0.359, 0.853, 0.000,0.404, 0.764, 0.014,0.416, 0.670, 0.030,0.421, 0.587, 0.038,0.415, 0.514, 0.048,0.289, 0.643, 0.084,0.314, 0.549, 0.092,0.359, 0.515, 0.093,0.400, 0.496, 0.094,0.251, 0.633, 0.065,0.219, 0.533, 0.082,0.219, 0.451, 0.078,0.223, 0.384, 0.071,0.220, 0.641, 0.038,0.164, 0.549, 0.049,0.144, 0.473, 0.048,0.138, 0.407, 0.043,0.199, 0.660, 0.009,0.130, 0.601, 0.011,0.095, 0.547, 0.010,0.074, 0.496, 0.010],
[0.256, 0.943, 0.000,0.346, 0.897, 0.008,0.411, 0.830, 0.022,0.460, 0.754, 0.028,0.473, 0.675, 0.034,0.329, 0.709, 0.101,0.382, 0.644, 0.122,0.426, 0.638, 0.127,0.461, 0.646, 0.130,0.293, 0.668, 0.087,0.314, 0.554, 0.122,0.346, 0.488, 0.121,0.375, 0.440, 0.115,0.256, 0.653, 0.064,0.252, 0.536, 0.091,0.267, 0.461, 0.091,0.287, 0.413, 0.085,0.222, 0.655, 0.037,0.198, 0.555, 0.051,0.195, 0.487, 0.053,0.199, 0.432, 0.053],
[0.232, 0.898, 0.000,0.308, 0.872, -0.015,0.380, 0.806, -0.023,0.436, 0.749, -0.036,0.476, 0.701, -0.047,0.346, 0.652, 0.015,0.411, 0.603, -0.010,0.450, 0.639, -0.024,0.473, 0.679, -0.030,0.315, 0.607, -0.004,0.354, 0.487, -0.019,0.393, 0.415, -0.035,0.423, 0.354, -0.050,0.273, 0.598, -0.031,0.287, 0.467, -0.052,0.309, 0.382, -0.066,0.332, 0.312, -0.078,0.229, 0.617, -0.064,0.215, 0.517, -0.086,0.214, 0.446, -0.097,0.219, 0.381, -0.105],
[0.499, 0.686, 0.000,0.550, 0.683, -0.005,0.595, 0.655, -0.005,0.631, 0.626, -0.009,0.656, 0.593, -0.011,0.566, 0.554, 0.024,0.610, 0.532, 0.017,0.637, 0.553, 0.013,0.653, 0.579, 0.011,0.552, 0.522, 0.014,0.578, 0.456, 0.012,0.607, 0.417, 0.004,0.632, 0.388, -0.004,0.532, 0.510, -0.000,0.541, 0.432, -0.006,0.559, 0.385, -0.011,0.580, 0.349, -0.016,0.510, 0.514, -0.018,0.509, 0.447, -0.025,0.516, 0.405, -0.029,0.529, 0.370, -0.032],
[0.354, 0.764, 0.000,0.395, 0.764, -0.013,0.435, 0.744, -0.017,0.463, 0.716, -0.021,0.474, 0.682, -0.023,0.414, 0.655, 0.011,0.445, 0.623, 0.005,0.461, 0.640, 0.003,0.469, 0.663, 0.002,0.399, 0.626, 0.008,0.421, 0.565, 0.008,0.443, 0.534, 0.003,0.461, 0.509, -0.002,0.381, 0.614, -0.000,0.389, 0.549, -0.003,0.404, 0.510, -0.007,0.420, 0.481, -0.012,0.361, 0.617, -0.011,0.359, 0.563, -0.017,0.364, 0.529, -0.020,0.373, 0.502, -0.022],
[0.258, 0.768, 0.000,0.318, 0.714, -0.017,0.357, 0.634, -0.018,0.374, 0.552, -0.021,0.372, 0.488, -0.023,0.268, 0.561, 0.034,0.291, 0.485, 0.029,0.327, 0.466, 0.025,0.360, 0.466, 0.022,0.227, 0.539, 0.028,0.223, 0.439, 0.033,0.233, 0.366, 0.023,0.243, 0.310, 0.012,0.189, 0.540, 0.015,0.161, 0.446, 0.015,0.155, 0.372, 0.006,0.158, 0.313, -0.003,0.156, 0.558, -0.003,0.113, 0.486, -0.009,0.094, 0.429, -0.015,0.085, 0.379, -0.020],
[0.283, 0.859, 0.000,0.347, 0.884, -0.015,0.420, 0.880, -0.024,0.477, 0.884, -0.037,0.523, 0.884, -0.048,0.447, 0.717, 0.004,0.518, 0.732, -0.020,0.535, 0.794, -0.033,0.536, 0.844, -0.041,0.437, 0.671, -0.013,0.511, 0.606, -0.031,0.573, 0.580, -0.049,0.624, 0.559, -0.066,0.408, 0.648, -0.037,0.463, 0.551, -0.059,0.513, 0.501, -0.076,0.560, 0.463, -0.089,0.369, 0.647, -0.065,0.389, 0.560, -0.087,0.414, 0.504, -0.099,0.445, 0.457, -0.108],
[0.184, 0.773, 0.000,0.262, 0.729, -0.019,0.320, 0.662, -0.016,0.355, 0.578, -0.015,0.359, 0.515, -0.011,0.246, 0.555, 0.042,0.288, 0.475, 0.045,0.322, 0.470, 0.044,0.351, 0.480, 0.044,0.206, 0.519, 0.040,0.222, 0.408, 0.052,0.242, 0.334, 0.045,0.261, 0.276, 0.035,0.165, 0.511, 0.029,0.156, 0.401, 0.034,0.164, 0.320, 0.023,0.180, 0.258, 0.013,0.125, 0.524, 0.013,0.095, 0.435, 0.010,0.088, 0.371, 0.003,0.089, 0.316, -0.003],
[0.664, 0.565, 0.000,0.631, 0.632, -0.069,0.579, 0.658, -0.113,0.525, 0.686, -0.133,0.481, 0.692, -0.146,0.570, 0.526, -0.180,0.492, 0.582, -0.214,0.471, 0.640, -0.217,0.472, 0.680, -0.219,0.556, 0.475, -0.147,0.462, 0.474, -0.216,0.394, 0.461, -0.248,0.343, 0.439, -0.267,0.551, 0.449, -0.103,0.470, 0.444, -0.152,0.410, 0.423, -0.177,0.364, 0.399, -0.190,0.549, 0.443, -0.057,0.480, 0.420, -0.083,0.436, 0.400, -0.101,0.405, 0.383, -0.115],
[0.462, 0.827, 0.000,0.387, 0.818, -0.085,0.350, 0.772, -0.136,0.311, 0.722, -0.160,0.285, 0.662, -0.180,0.451, 0.709, -0.207,0.392, 0.640, -0.249,0.332, 0.621, -0.263,0.290, 0.626, -0.272,0.477, 0.666, -0.165,0.476, 0.558, -0.245,0.474, 0.463, -0.290,0.483, 0.392, -0.320,0.493, 0.645, -0.113,0.498, 0.552, -0.174,0.504, 0.471, -0.215,0.517, 0.412, -0.239,0.497, 0.635, -0.058,0.517, 0.566, -0.097,0.542, 0.522, -0.127,0.569, 0.496, -0.147],
[0.444, 0.679, 0.000,0.393, 0.629, -0.071,0.377, 0.581, -0.121,0.366, 0.522, -0.147,0.375, 0.469, -0.169,0.480, 0.609, -0.195,0.457, 0.520, -0.242,0.416, 0.469, -0.257,0.377, 0.449, -0.268,0.519, 0.586, -0.166,0.566, 0.503, -0.251,0.608, 0.430, -0.296,0.647, 0.387, -0.326,0.538, 0.578, -0.126,0.580, 0.505, -0.194,0.619, 0.448, -0.233,0.654, 0.413, -0.254,0.545, 0.570, -0.084,0.591, 0.536, -0.129,0.626, 0.521, -0.157,0.656, 0.517, -0.175],
[0.285, 0.762, 0.000,0.344, 0.757, -0.029,0.409, 0.722, -0.041,0.461, 0.686, -0.053,0.499, 0.653, -0.065,0.399, 0.582, -0.005,0.462, 0.549, -0.028,0.490, 0.586, -0.041,0.503, 0.625, -0.049,0.376, 0.535, -0.013,0.422, 0.437, -0.027,0.456, 0.378, -0.047,0.480, 0.322, -0.065,0.341, 0.521, -0.029,0.360, 0.409, -0.050,0.374, 0.337, -0.072,0.385, 0.277, -0.089,0.300, 0.531, -0.050,0.284, 0.442, -0.072,0.271, 0.383, -0.087,0.263, 0.329, -0.099],
[0.432, 0.845, 0.000,0.379, 0.744, 0.030,0.374, 0.651, 0.043,0.401, 0.577, 0.052,0.438, 0.538, 0.063,0.424, 0.577, 0.021,0.446, 0.511, 0.027,0.454, 0.531, 0.041,0.459, 0.562, 0.051,0.468, 0.580, -0.000,0.498, 0.460, 0.007,0.520, 0.396, 0.018,0.541, 0.344, 0.021,0.504, 0.606, -0.020,0.542, 0.496, -0.015,0.568, 0.435, -0.007,0.592, 0.386, -0.006,0.534, 0.652, -0.037,0.568, 0.574, -0.038,0.591, 0.530, -0.034,0.614, 0.489, -0.031],
[0.420, 0.806, 0.000,0.334, 0.813, -0.063,0.247, 0.766, -0.101,0.163, 0.716, -0.119,0.108, 0.668, -0.131,0.301, 0.604, -0.146,0.176, 0.548, -0.173,0.113, 0.592, -0.176,0.087, 0.643, -0.177,0.326, 0.545, -0.122,0.217, 0.421, -0.171,0.147, 0.330, -0.199,0.110, 0.247, -0.223,0.348, 0.530, -0.091,0.280, 0.404, -0.126,0.245, 0.310, -0.152,0.225, 0.233, -0.171,0.366, 0.542, -0.060,0.348, 0.438, -0.081,0.356, 0.363, -0.097,0.367, 0.304, -0.110],
[0.233, 0.748, 0.000,0.308, 0.723, 0.012,0.369, 0.653, 0.024,0.425, 0.602, 0.026,0.479, 0.566, 0.029,0.332, 0.522, 0.077,0.397, 0.488, 0.075,0.444, 0.516, 0.071,0.479, 0.546, 0.070,0.313, 0.477, 0.053,0.345, 0.370, 0.062,0.385, 0.313, 0.054,0.419, 0.268, 0.044,0.286, 0.457, 0.021,0.297, 0.326, 0.023,0.315, 0.248, 0.017,0.334, 0.186, 0.011,0.260, 0.457, -0.015,0.247, 0.346, -0.019,0.243, 0.271, -0.021,0.244, 0.204, -0.024],
[0.391, 0.786, 0.000,0.433, 0.690, 0.029,0.447, 0.597, 0.049,0.456, 0.511, 0.056,0.439, 0.441, 0.065,0.305, 0.575, 0.105,0.332, 0.475, 0.115,0.386, 0.440, 0.116,0.434, 0.425, 0.117,0.267, 0.560, 0.076,0.224, 0.451, 0.093,0.223, 0.359, 0.088,0.225, 0.280, 0.080,0.238, 0.563, 0.038,0.172, 0.463, 0.050,0.143, 0.376, 0.048,0.125, 0.297, 0.042,0.222, 0.577, -0.002,0.144, 0.510, 0.001,0.098, 0.452, 0.001,0.064, 0.398, -0.001],
[0.197, 0.777, 0.000,0.287, 0.777, -0.011,0.375, 0.725, -0.012,0.447, 0.679, -0.018,0.509, 0.644, -0.023,0.360, 0.570, 0.039,0.438, 0.544, 0.024,0.480, 0.577, 0.014,0.506, 0.619, 0.009,0.337, 0.505, 0.022,0.405, 0.403, 0.017,0.463, 0.347, 0.002,0.511, 0.303, -0.013,0.299, 0.469, -0.004,0.343, 0.338, -0.016,0.386, 0.264, -0.030,0.425, 0.208, -0.040,0.254, 0.459, -0.034,0.266, 0.339, -0.050,0.283, 0.263, -0.059,0.303, 0.199, -0.066],
[0.306, 0.701, 0.000,0.300, 0.710, -0.098,0.313, 0.688, -0.148,0.312, 0.633, -0.180,0.325, 0.582, -0.208,0.420, 0.650, -0.115,0.487, 0.624, -0.165,0.536, 0.597, -0.198,0.577, 0.578, -0.218,0.401, 0.610, -0.080,0.393, 0.526, -0.142,0.333, 0.562, -0.155,0.320, 0.599, -0.150,0.378, 0.578, -0.052,0.351, 0.522, -0.109,0.310, 0.561, -0.117,0.313, 0.602, -0.111,0.360, 0.555, -0.032,0.340, 0.517, -0.069,0.312, 0.547, -0.081,0.317, 0.576, -0.082],
[0.321, 0.740, 0.000,0.372, 0.725, -0.027,0.409, 0.677, -0.045,0.399, 0.618, -0.064,0.372, 0.571, -0.080,0.414, 0.555, -0.023,0.441, 0.460, -0.048,0.458, 0.400, -0.066,0.471, 0.350, -0.077,0.370, 0.547, -0.027,0.365, 0.499, -0.062,0.357, 0.578, -0.063,0.357, 0.631, -0.054,0.328, 0.555, -0.037,0.321, 0.530, -0.066,0.326, 0.609, -0.054,0.334, 0.655, -0.040,0.292, 0.575, -0.051,0.289, 0.549, -0.068,0.300, 0.603, -0.062,0.312, 0.637, -0.052],
[0.287, 0.826, 0.000,0.336, 0.795, -0.030,0.367, 0.731, -0.060,0.351, 0.682, -0.091,0.304, 0.659, -0.118,0.322, 0.587, -0.047,0.306, 0.474, -0.084,0.294, 0.410, -0.107,0.280, 0.355, -0.122,0.270, 0.596, -0.056,0.256, 0.580, -0.100,0.280, 0.671, -0.102,0.298, 0.722, -0.093,0.229, 0.627, -0.069,0.227, 0.659, -0.104,0.260, 0.735, -0.095,0.283, 0.765, -0.083,0.197, 0.667, -0.088,0.202, 0.701, -0.105,0.235, 0.756, -0.101,0.259, 0.774, -0.094],
[0.296, 0.803, 0.000,0.348, 0.777, -0.024,0.388, 0.722, -0.048,0.374, 0.673, -0.073,0.336, 0.639, -0.096,0.371, 0.588, -0.037,0.389, 0.479, -0.067,0.400, 0.414, -0.086,0.406, 0.357, -0.100,0.321, 0.581, -0.045,0.312, 0.555, -0.080,0.314, 0.635, -0.082,0.320, 0.693, -0.076,0.277, 0.596, -0.056,0.268, 0.612, -0.083,0.284, 0.687, -0.075,0.299, 0.733, -0.065,0.241, 0.622, -0.073,0.236, 0.640, -0.085,0.256, 0.696, -0.081,0.275, 0.730, -0.074],
[0.585, 0.682, 0.000,0.646, 0.668, -0.004,0.700, 0.630, -0.017,0.729, 0.587, -0.036,0.731, 0.537, -0.053,0.691, 0.505, -0.005,0.727, 0.422, -0.031,0.746, 0.370, -0.049,0.760, 0.324, -0.061,0.652, 0.487, -0.023,0.693, 0.450, -0.058,0.691, 0.527, -0.061,0.680, 0.583, -0.054,0.614, 0.485, -0.044,0.653, 0.488, -0.075,0.645, 0.569, -0.065,0.629, 0.615, -0.050,0.575, 0.493, -0.068,0.612, 0.495, -0.086,0.611, 0.556, -0.079,0.599, 0.592, -0.068],
[0.273, 0.840, 0.000,0.313, 0.796, -0.024,0.333, 0.729, -0.048,0.307, 0.694, -0.073,0.264, 0.684, -0.096,0.282, 0.617, -0.035,0.262, 0.520, -0.064,0.246, 0.464, -0.084,0.231, 0.418, -0.098,0.237, 0.636, -0.042,0.221, 0.624, -0.078,0.245, 0.693, -0.080,0.266, 0.738, -0.075,0.204, 0.670, -0.054,0.200, 0.689, -0.081,0.235, 0.747, -0.073,0.259, 0.778, -0.063,0.180, 0.711, -0.070,0.183, 0.729, -0.083,0.215, 0.768, -0.078,0.238, 0.787, -0.072],
[0.315, 0.799, 0.000,0.362, 0.771, -0.013,0.399, 0.706, -0.027,0.402, 0.646, -0.045,0.381, 0.596, -0.062,0.377, 0.599, -0.007,0.385, 0.506, -0.033,0.386, 0.452, -0.049,0.386, 0.405, -0.059,0.337, 0.603, -0.020,0.344, 0.541, -0.056,0.355, 0.611, -0.059,0.359, 0.662, -0.050,0.298, 0.621, -0.037,0.311, 0.590, -0.070,0.325, 0.666, -0.058,0.326, 0.708, -0.040,0.260, 0.650, -0.058,0.273, 0.614, -0.078,0.292, 0.665, -0.070,0.299, 0.699, -0.058],
[0.376, 0.710, 0.000,0.424, 0.708, -0.029,0.474, 0.682, -0.059,0.479, 0.655, -0.089,0.445, 0.629, -0.116,0.481, 0.541, -0.064,0.515, 0.438, -0.100,0.535, 0.378, -0.124,0.550, 0.323, -0.139,0.433, 0.514, -0.068,0.429, 0.520, -0.106,0.419, 0.612, -0.103,0.416, 0.669, -0.095,0.390, 0.512, -0.076,0.383, 0.550, -0.104,0.387, 0.631, -0.091,0.392, 0.676, -0.080,0.352, 0.525, -0.088,0.350, 0.554, -0.101,0.359, 0.616, -0.093,0.368, 0.654, -0.086],
[0.474, 0.660, 0.000,0.516, 0.673, -0.043,0.561, 0.681, -0.091,0.582, 0.689, -0.137,0.578, 0.682, -0.181,0.614, 0.544, -0.111,0.682, 0.473, -0.173,0.724, 0.422, -0.212,0.757, 0.377, -0.238,0.568, 0.497, -0.118,0.583, 0.535, -0.183,0.558, 0.631, -0.187,0.540, 0.689, -0.182,0.520, 0.481, -0.127,0.527, 0.553, -0.177,0.518, 0.636, -0.165,0.509, 0.678, -0.152,0.475, 0.484, -0.142,0.487, 0.543, -0.168,0.485, 0.607, -0.162,0.482, 0.640, -0.155],
[0.297, 0.714, 0.000,0.333, 0.750, -0.054,0.366, 0.770, -0.110,0.354, 0.779, -0.157,0.327, 0.784, -0.201,0.388, 0.630, -0.128,0.409, 0.582, -0.199,0.415, 0.531, -0.241,0.416, 0.486, -0.264,0.348, 0.585, -0.122,0.323, 0.659, -0.185,0.303, 0.740, -0.183,0.301, 0.766, -0.176,0.304, 0.582, -0.120,0.283, 0.679, -0.171,0.282, 0.754, -0.155,0.290, 0.779, -0.138,0.267, 0.595, -0.124,0.245, 0.681, -0.150,0.249, 0.741, -0.141,0.262, 0.762, -0.133],
[0.329, 0.862, 0.000,0.300, 0.758, 0.045,0.316, 0.677, 0.057,0.354, 0.638, 0.059,0.388, 0.637, 0.065,0.335, 0.601, 0.024,0.361, 0.498, 0.030,0.384, 0.432, 0.034,0.400, 0.380, 0.036,0.383, 0.605, 0.001,0.413, 0.611, 0.020,0.409, 0.650, 0.041,0.394, 0.677, 0.051,0.425, 0.641, -0.018,0.436, 0.661, 0.007,0.428, 0.691, 0.026,0.413, 0.709, 0.031,0.461, 0.684, -0.036,0.464, 0.705, -0.014,0.452, 0.733, -0.000,0.437, 0.751, 0.006],
[0.397, 0.804, 0.000,0.344, 0.734, 0.022,0.330, 0.652, 0.023,0.357, 0.592, 0.020,0.390, 0.568, 0.020,0.327, 0.586, -0.012,0.318, 0.459, -0.019,0.318, 0.379, -0.022,0.317, 0.319, -0.023,0.378, 0.574, -0.025,0.404, 0.521, -0.016,0.411, 0.562, 0.004,0.406, 0.601, 0.015,0.425, 0.587, -0.036,0.440, 0.569, -0.022,0.439, 0.603, -0.002,0.431, 0.631, 0.007,0.469, 0.606, -0.048,0.468, 0.597, -0.036,0.467, 0.630, -0.024,0.463, 0.653, -0.016],
[0.277, 0.800, 0.000,0.224, 0.728, 0.031,0.195, 0.649, 0.028,0.206, 0.585, 0.018,0.235, 0.552, 0.012,0.157, 0.599, -0.011,0.112, 0.490, -0.026,0.083, 0.421, -0.033,0.059, 0.367, -0.038,0.193, 0.578, -0.037,0.251, 0.500, -0.038,0.273, 0.533, -0.021,0.269, 0.565, -0.012,0.244, 0.574, -0.059,0.303, 0.529, -0.055,0.309, 0.568, -0.033,0.296, 0.595, -0.023,0.300, 0.576, -0.082,0.341, 0.548, -0.076,0.344, 0.585, -0.063,0.334, 0.611, -0.054],
[0.279, 0.636, 0.000,0.341, 0.550, 0.059,0.408, 0.519, 0.066,0.465, 0.542, 0.061,0.493, 0.583, 0.059,0.476, 0.477, 0.015,0.572, 0.453, 0.004,0.637, 0.431, -0.006,0.687, 0.411, -0.013,0.495, 0.516, -0.020,0.538, 0.623, -0.014,0.500, 0.651, 0.003,0.469, 0.645, 0.011,0.496, 0.583, -0.050,0.515, 0.685, -0.039,0.471, 0.700, -0.019,0.443, 0.686, -0.013,0.489, 0.653, -0.079,0.498, 0.745, -0.064,0.462, 0.757, -0.049,0.440, 0.757, -0.043],
[0.237, 0.620, 0.000,0.315, 0.541, 0.059,0.393, 0.516, 0.067,0.455, 0.538, 0.061,0.487, 0.579, 0.059,0.458, 0.466, 0.021,0.560, 0.445, 0.010,0.626, 0.426, 0.001,0.676, 0.409, -0.007,0.469, 0.497, -0.017,0.530, 0.608, -0.014,0.493, 0.642, 0.001,0.460, 0.635, 0.006,0.464, 0.558, -0.050,0.499, 0.668, -0.040,0.458, 0.683, -0.023,0.431, 0.662, -0.018,0.452, 0.624, -0.082,0.470, 0.719, -0.068,0.433, 0.725, -0.055,0.409, 0.710, -0.049],
[0.516, 0.721, 0.000,0.441, 0.781, -0.080,0.352, 0.776, -0.108,0.290, 0.724, -0.105,0.239, 0.664, -0.099,0.375, 0.613, -0.171,0.287, 0.484, -0.207,0.243, 0.400, -0.221,0.209, 0.334, -0.223,0.401, 0.566, -0.107,0.309, 0.554, -0.105,0.306, 0.623, -0.071,0.319, 0.660, -0.050,0.417, 0.545, -0.042,0.340, 0.543, -0.038,0.335, 0.604, -0.012,0.348, 0.640, 0.003,0.422, 0.530, 0.018,0.363, 0.530, 0.018,0.356, 0.577, 0.026,0.357, 0.614, 0.034],
[0.235, 0.781, 0.000,0.295, 0.764, -0.027,0.342, 0.705, -0.046,0.340, 0.623, -0.066,0.320, 0.555, -0.085,0.357, 0.585, -0.019,0.397, 0.487, -0.047,0.421, 0.426, -0.066,0.441, 0.373, -0.080,0.309, 0.568, -0.027,0.310, 0.510, -0.066,0.293, 0.598, -0.069,0.288, 0.664, -0.061,0.263, 0.571, -0.040,0.259, 0.544, -0.075,0.255, 0.639, -0.064,0.258, 0.699, -0.049,0.222, 0.591, -0.060,0.224, 0.570, -0.080,0.227, 0.641, -0.074,0.235, 0.689, -0.063],
[0.323, 0.900, 0.000,0.295, 0.778, 0.053,0.320, 0.675, 0.070,0.365, 0.619, 0.077,0.404, 0.607, 0.087,0.356, 0.601, 0.031,0.385, 0.479, 0.041,0.410, 0.405, 0.050,0.426, 0.347, 0.055,0.413, 0.622, 0.006,0.435, 0.618, 0.032,0.426, 0.659, 0.061,0.408, 0.691, 0.077,0.458, 0.680, -0.013,0.464, 0.694, 0.015,0.451, 0.729, 0.039,0.432, 0.751, 0.048,0.494, 0.745, -0.032,0.489, 0.766, -0.008,0.471, 0.799, 0.009,0.451, 0.823, 0.017],
[0.240, 0.816, 0.000,0.231, 0.681, 0.041,0.255, 0.574, 0.039,0.313, 0.517, 0.029,0.364, 0.509, 0.023,0.242, 0.486, -0.015,0.289, 0.336, -0.035,0.316, 0.240, -0.046,0.336, 0.165, -0.053,0.283, 0.499, -0.045,0.392, 0.463, -0.041,0.395, 0.525, -0.015,0.372, 0.558, -0.003,0.329, 0.541, -0.072,0.417, 0.542, -0.058,0.405, 0.593, -0.027,0.376, 0.613, -0.014,0.378, 0.589, -0.098,0.434, 0.600, -0.085,0.422, 0.645, -0.065,0.396, 0.661, -0.054],
[0.237, 0.903, 0.000,0.335, 0.832, 0.016,0.398, 0.734, -0.003,0.436, 0.647, -0.034,0.453, 0.561, -0.059,0.283, 0.532, 0.029,0.299, 0.420, -0.009,0.295, 0.334, -0.041,0.285, 0.259, -0.064,0.246, 0.531, -0.008,0.390, 0.498, -0.058,0.402, 0.623, -0.064,0.368, 0.674, -0.059,0.231, 0.559, -0.051,0.378, 0.563, -0.097,0.372, 0.685, -0.081,0.325, 0.723, -0.062,0.227, 0.599, -0.096,0.351, 0.621, -0.120,0.346, 0.716, -0.107,0.296, 0.748, -0.09]
]


def read_csv_file(file_path):
    data = pd.read_csv(file_path, index_col=0)
    return data
# Example usage
csv_file_path = "test.csv"
hand_motions = read_csv_file(csv_file_path)
#hand_motions = np.array(hand_motions)


answer = [[1,0,0],
          [0,1,0],
          [0,0,1]]
answer = [i for i in answer for _ in range(40)]


# 데이터를 특성과 레이블로 분할
X = np.array(hand_motions)
y = np.array(answer)

# 데이터를 학습과 테스트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

# 모델 정의
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(63,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 모델 학습
model.fit(X_train, y_train, epochs=1000)

# 모델 평가
model.evaluate(X_test, y_test)

model.save('./model_h5/hand_model.h5')
model.save_weights('./model_w/hand_model_weight')