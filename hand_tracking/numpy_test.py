import numpy as np



# initialize our 2D array
arr2d = []
# append a 1D array to our 2D array
new_row = np.array([7, 8, 9])
arr2d = np.append(arr2d, np.array([7.7,8.8,9.9]), axis=0)
#arr2d = np.concatenate(arr2d, new_row)
arr2d = np.vstack((arr2d, new_row))
print(arr2d)  


# prints: [[1 2 3]
#          [4 5 6]
#          [7 8 9]]


#arr2d = [[1, 2, 3], [4, 5, 6]]

#arrnp = np.array(arr2d).reshape(1,-1)
#print(arrnp)