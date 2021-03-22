import random
import itertools
import math
# import matplotlib.pyplot as plt
import pickle
from pipe import *


N = 20
MAX_WEIGHT = 30
weights = random.choices(range(1, 10), k=N)
values  = random.choices(range(1, 10), k=N)


print(weights)
print(values)


def random_mask():
    return random.choices(range(0, 2), k=N)


def evaluate(mask):
    _ = zip(weights, values)
    _ = itertools.compress(_, mask) | Pipe(list)
    
    if not _:
        return 0
    
    w, v = zip(*_)
    
    weight = sum(w)
    if sum(w) > MAX_WEIGHT:
        return 0
    return sum(v)


def mask_to_int(mask):
    return (
        zip(mask, range(len(mask) - 1, -1, -1))
        | MapValues(lambda x: 2 ** x)
        | Map(math.prod)
        | Pipe(sum)
    )


def check_mask(x):
    k, v = random_mask() | Pipe(lambda x: (x, x))
    return evaluate(k), mask_to_int(v)


# def mean(n):
#     return sum(range(n)) / n


def main():
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = pool.map(check_mask, range(1, 40_000), chunksize=5000) | FilterKeys(bool)
        V, I = zip(*result)

if __name__ == '__main__':
 
    main()

    # print(V[:3], I[:3])


with open('IV.pkl', 'wb') as fd:
    pickle.dump((I, V), fd)


# # 2 ** N
# it = (
# # V, I = zip(*
#     range(30_000)
#     | Map(lambda x: random_mask())
#     | Map(lambda x: (x, x))
#     | MapKeys(evaluate)
#     | MapValues(mask_to_int)
#     | FilterKeys(bool)
#     # | Pipe(list)
# )

# plt.figure(figsize=(12, 7))
# plt.grid(lw=0.2)
# plt.scatter(I, V, s=2)





