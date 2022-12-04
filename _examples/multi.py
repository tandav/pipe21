import itertools
import collections
import concurrent.futures
from pipe import *

def task(i):
    return itertools.combinations(range(16), i) | Map(sum) | Pipe(list) | Pipe(collections.Counter)


if __name__ == '__main__':
    # res = range(16) | ThreadMap(task)
    res = range(16) | ProcessMap(task)
    print(res)
