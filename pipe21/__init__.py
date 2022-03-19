import concurrent.futures
import itertools
import operator
import re
import subprocess
from functools import partial
from functools import reduce


class B:
    def __init__(self, f=None, **kw): self.f = f; self.kw = kw
class Pipe  (B): __ror__ = lambda self, x: self.f(x)
class Map   (B): __ror__ = lambda self, x: map   (self.f, x)
class Filter(B): __ror__ = lambda self, x: filter(self.f, x)


class Reduce        (B): __ror__ = lambda self, x: reduce(self.f, x)
class MapValues     (B): __ror__ = lambda self, it: it | Map(lambda kv: (kv[0], self.f(kv[1])))
class MapKeys       (B): __ror__ = lambda self, it: it | Map(lambda kv: (self.f(kv[0]), kv[1]))
class FilterFalse   (B): __ror__ = lambda self, it: it | Filter(lambda x: not self.f(x))
class FilterKeys    (B): __ror__ = lambda self, it: it | Filter(operator.itemgetter(0))
class FilterValues  (B): __ror__ = lambda self, it: it | Filter(operator.itemgetter(1))
class FlatMap       (B): __ror__ = lambda self, it: it | Map(self.f) | Pipe(itertools.chain.from_iterable)
class FlatMapValues (B): __ror__ = lambda self, it: it | FlatMap(lambda kv: ((kv[0], x) for x in self.f(kv[1])))
class KeyBy         (B): __ror__ = lambda self, it: it | Map(lambda x: (self.f(x), x))
class ValueBy       (B): __ror__ = lambda self, it: it | Map(lambda x: (x, self.f(x)))
class Append        (B): __ror__ = lambda self, it: it | Map(lambda x: (*x, self.f(x)))
class Keys          (B): __ror__ = lambda self, it: it | Map(operator.itemgetter(0))
class Values        (B): __ror__ = lambda self, it: it | Map(operator.itemgetter(1))
class Grep          (B): __ror__ = lambda self, it: it | Filter(lambda x:     re.search(self.f, x))
class GrepV         (B): __ror__ = lambda self, it: it | Filter(lambda x: not re.search(self.f, x))
class FilterEqual   (B): __ror__ = lambda self, it: it | Filter(lambda x: x == self.f)
class FilterNotEqual(B): __ror__ = lambda self, it: it | Filter(lambda x: x != self.f)
class Count         (B): __ror__ = lambda self, it: sum(1 for _ in it)
class Take          (B): __ror__ = lambda self, it: itertools.islice(it, self.f) | Pipe(tuple)
class Chunked       (B): __ror__ = lambda self, it: iter(partial(lambda n, i: i | Take(n), self.f, iter(it)), ())
class GroupBy       (B): __ror__ = lambda self, it: itertools.groupby(it, key=self.f)
class ReadLines     (B): __ror__ = lambda self, fn: open(fn).readlines()
class ShellExec     (B): __ror__ = lambda self, x: subprocess.check_output(         x , text=True).splitlines()
class PipeArgs      (B): __ror__ = lambda self, x: self.f(*x)
class MapArgs       (B): __ror__ = lambda self, x: x | Map(lambda y: y | PipeArgs(self.f))
class IsUnique      (B): __ror__ = lambda self, seq: len(seq) == len(set(seq if self.f is None else map(self.f, seq)))
class Sorted        (B): __ror__ = lambda self, it: sorted(it, **self.kw)


class Unique(B):
    def __ror__(self, it):
        key = self.f or (lambda x: x)
        seen = set()
        for item in it:
            k = key(item)
            if k in seen:
                continue
            seen.add(k)
            yield item


class ForEach(B):
    def __ror__(self, x):
        for e in x: self.f(e)


class ThreadMap(B):
    def __ror__(self, it):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.map(self.f, it) | Pipe(tuple)


class ProcessMap(B):
    def __ror__(self, it):
        with concurrent.futures.ProcessPoolExecutor() as pool:
            return pool.map(self.f, it) | Pipe(tuple)
