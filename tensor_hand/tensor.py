import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib as plt

from sklearn.model_selection import train_test_split

# 데이터 불러오기
def read_csv_file(file_path):
    data = pd.read_csv(file_path, index_col=0)
    return data

csv_file_path = "test.csv"
hand_motions = read_csv_file(csv_file_path)

answer = [[1,0,0,0],
          [0,1,0,0],
          [0,0,1,0],
          [0,0,0,1]]
answer = [i for i in answer for _ in range(30)]

# 데이터를 특성과 레이블로 분할
X = np.array(hand_motions)
y = np.array(answer)

# 데이터를 학습과 테스트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

# 모델 정의
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(63,)),
    tf.keras.layers.Dropout(0.5),#과적합 방지
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(4, activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 모델 학습
model.fit(X_train, y_train, epochs=500, batch_size=32, validation_split=0.2)

# 모델 평가
model.evaluate(X_test, y_test)

model.save('./model_h5/hand_model.h5')
model.save_weights('./model_w/hand_model_weight')
