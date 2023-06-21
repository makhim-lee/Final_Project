import numpy as np
import pandas as pd

button1 = np.array([[17, 26, 83, 62], [17, 57, 83, 73]])
button2 = np.array([[3, 4, 6, 1]])

data = {
    'name': ['restaurant', 'hope',],
    'button_list': [['Steak', 'Shake', ], ['soju',]],
    'button_np': [button1, button2]
}
IP = [101, 102]
df = pd.DataFrame(data, index=IP)

a, b, c = df.loc[101]
print(a)


# print(df.loc[1, 'Column1'])
# print(df.loc[2, 'Column1'])
# print(type(df.loc[2, 'Column1']))
