import random
from pipe import *
import collections
import statistics
import matplotlib.pyplot as plt
import concurrent.futures
import itertools
import operator


n_machines = 10

machines = [
    (random.random(), random.random(), m) # probability reward machine
    for m in range(n_machines)
]


def eval_session(eps, n_steps=2048):
    # print(f'{eps} start')

    history = collections.defaultdict(list)
    R = 0

    for i in range(n_steps):
        if history and random.random() > eps:
            # greedy
            m, V = max(history.items(), key=lambda kV: statistics.fmean(kV[1]))
            p, r, m = machines[m]
        else:
            # exploration
            p, r, m = random.choice(machines)
        _r = r if random.random() > p else 0
        R += _r
        history[m].append(_r)
    print(f'{eps} done')
    return eps, R


def it_random(n):
    for _ in range(n):
        yield random.random()


def main():
    result = (
        it_random(5000)
        | Pipe(sorted)
        | ProcessMap(eval_session)
        | GroupBy(lambda x: round(x[0], 3))
        | MapValues(lambda er: sum(r for e, r in er))
        # | Pipe(list)
    )

    E, R = zip(*result)
    # it = map(lambda er: (round(er[0], 2), er[1]), result)
    # C = collections.defaultdict(float)
    # for e, r in result:
    #     C[round(e, 3)] += r

    # E, R = zip(*sorted(C.items()))
    plt.figure(figsize=(16, 5))
    plt.plot(E, R)
    plt.tight_layout()
    plt.savefig('image.png')
    # with open('ER.txt', 'w') as fd:
    #     for e, r in sorted(C.items()):
    #         print(e, r, sep=',', file=fd)

if __name__ == '__main__':
    main()





