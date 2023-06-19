'''
import multiprocessing

class SquareCalculator:
    def calculate_square(self, n):
        return n * n

def worker_method(obj, n):
    return obj.calculate_square(n)

calculator = SquareCalculator()
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
with multiprocessing.Pool() as pool:
    results = pool.starmap(worker_method, [(calculator, n) for n in data])
for result in results:
    print(result)

from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
'''
from multiprocessing import Process, Queue

def producer(queue):
    for i in range(10):
        print(f'Producer putting {i} into queue')
        queue.put(i)

def consumer(queue):
    for _ in range(10):
        item = queue.get()
        print(f'Consumer got {item} from queue')

if __name__ == "__main__":
    queue = Queue()

    p1 = Process(target=producer, args=(queue,))
    p2 = Process(target=consumer, args=(queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
