import numpy as np
import pandas as pd

numpy_test1 = np.array([[1,2,3,4],[2,3,4,5]])
numpy_test2 = np.array([[3,4,6,1],[2,7,8,9]])

data = {
    'name': ['coff', 'hope',],
    'butten_list': [['cola','coffee',''], ['e','d','f']],
    'butten_np': [numpy_test1, numpy_test2]
}
IP = [101,102]
df = pd.DataFrame(data,index=IP)

print(df)

#print(df.loc[1, 'Column1'])
#print(df.loc[2, 'Column1'])
#print(type(df.loc[2, 'Column1']))

