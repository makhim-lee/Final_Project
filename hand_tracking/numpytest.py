import numpy as np

import tensorflow as tf

print(tf.__version__)

model = tf.keras.models.load_model('hand_model.h5')
print(model)
#for i in range(1,4):
#    data = []
#    for i in range(i, 5):
#        data.append([i,i+1,i+2])
#
#    np_data = np.array(data)
#    print(np_data)
    
    
    #input_data = np_data.reshape(1, -1)
    #print(input_data)