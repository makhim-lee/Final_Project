import numpy as np
import pandas as pd
#def read_csv_file(file_path):
#    data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
#    return data

def read_csv_file(file_path):
    data = pd.read_csv(file_path, index_col=0)
    return data
# Example usage
csv_file_path = "test.csv"
hand_motions = read_csv_file(csv_file_path)
hand_motions = np.array(hand_motions)
print(hand_motions)
print(hand_motions.shape)