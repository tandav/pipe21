import random
from pipe import *
import collections
import statistics
import matplotlib.pyplot as plt
import concurrent.futures
import itertools
import operator
GREEN_STRING = lambda s: '\033[32m' + str(s) + '\033[0m'

# n = 50_000
# n = 500
# n = 10_000
n = 1_000

n_machines = 10

machines = [
    (random.random(), random.random(), m) # probability reward machine
    for m in range(n_machines)
]


# def eval_session(eps, n_steps=2048):
def eval_session(x, n_steps=2048):
    j, eps = x
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
    if j % 1000 == 0:
        print(f'{j:>5} / {n:>5} done')
    return eps, R


def it_random(n):
    for _ in range(n):
        yield random.random()



def main():

    result = (
        it_random(n)
        # | Pipe(sorted)
        | Pipe(enumerate)
        | ProcessMap(eval_session)
        | MapKeys(lambda x: round(x, 2))
        # | GroupBy(lambda x: round(x[0], 2))
        # | MapValues(lambda er: sum(r for e, r in er))
        # | Pipe(list)
        # | ForEach(lambda er: print(*er))
    )

    E, R = zip(*result)
    min_, max_ = min(R), max(R)

    C = collections.defaultdict(float)
    for e, r in zip(E, R):
        C[e] += r

    print(C)

    # print(min_, max_)

    # print(result)
    n_bars = 16

    for e, r in sorted(C.items()):
        qq = (r - min_) / (max_ - min_)
        # q = int(qq * 10)

        b = round(qq * n_bars)
        print(qq, b)
        s = f'{e:5.2f} ' + '=' * b# + '|'
        s = f'{s:<66}'
        if r == max_:
            s = GREEN_STRING(s)
        print(s, qq)


    # for e, r in result:
    #     print(e, r)

    # E, R = zip(*result)
    # it = map(lambda er: (round(er[0], 2), er[1]), result)
    # C = collections.defaultdict(float)
    # for e, r in result:
    #     C[round(e, 3)] += r

    # E, R = zip(*sorted(C.items()))
    # plt.figure(figsize=(16, 5))
    # plt.plot(E, R)
    # plt.tight_layout()
    # plt.savefig('image.png')
    # with open('ER.txt', 'w') as fd:
    #     for e, r in sorted(C.items()):
    #         print(e, r, sep=',', file=fd)

if __name__ == '__main__':
    main()





