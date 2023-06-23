import numpy as np
import pandas as pd
#def read_csv_file(file_path):
#    data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
#    return data
#ids = np.array([[5]])
#
#index = None
#index = np.where(ids == 1)[0]
#print(len(index)    )
import time

class Debouncer:
    def __init__(self, delay = 3):
        self.delay = delay
        self.last_exec = 0

    def should_execute(self):
        now = time.time()
        if now - self.last_exec > self.delay:
            self.last_exec = now
            return True
        return False
    

De = Debouncer()
while True:
    print("A")
    time.sleep(1)
    if De.should_execute():
        print("good")
    else :
        print("bad")