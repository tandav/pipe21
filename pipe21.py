import functools
import itertools
import re

__version__ = '1.9.0'


class B:
    def __init__(self, f=None, *args, **kw):
        self.f = f
        self.args = args
        self.kw = kw


class Pipe         (B): __ror__ = lambda self, x: self.f(x)
class Map          (B): __ror__ = lambda self, it: map(self.f, it)
class Filter       (B): __ror__ = lambda self, it: filter(self.f, it)
class Reduce       (B): __ror__ = lambda self, it: functools.reduce(self.f, it, *self.args)
class MapValues    (B): __ror__ = lambda self, it: it | Map(lambda kv: (kv[0], self.f(kv[1])))
class MapKeys      (B): __ror__ = lambda self, it: it | Map(lambda kv: (self.f(kv[0]), kv[1]))
class FilterFalse  (B): __ror__ = lambda self, it: it | Filter(lambda x: not self.f(x))
class FilterKeys   (B): __ror__ = lambda self, it: it | Filter(lambda x: (self.f or bool)(x[0]))
class FilterValues (B): __ror__ = lambda self, it: it | Filter(lambda x: (self.f or bool)(x[1]))
class FlatMap      (B): __ror__ = lambda self, it: it | Map(self.f) | Pipe(itertools.chain.from_iterable)
class FlatMapValues(B): __ror__ = lambda self, it: it | FlatMap(lambda kv: ((kv[0], x) for x in self.f(kv[1])))
class KeyBy        (B): __ror__ = lambda self, it: it | Map(lambda x: (self.f(x), x))
class ValueBy      (B): __ror__ = lambda self, it: it | Map(lambda x: (x, self.f(x)))
class Append       (B): __ror__ = lambda self, it: it | Map(lambda x: (*x, self.f(x)))
class Keys         (B): __ror__ = lambda self, it: it | Map(lambda x: x[0])
class Values       (B): __ror__ = lambda self, it: it | Map(lambda x: x[1])
class Grep         (B): __ror__ = lambda self, it: it | Filter(lambda x: re.search(self.f, x))
class GrepV        (B): __ror__ = lambda self, it: it | Filter(lambda x: not re.search(self.f, x))
class Count        (B): __ror__ = lambda self, it: sum(1 for _ in it)
class Slice        (B): __ror__ = lambda self, it: itertools.islice(it, self.f, *self.args)
class Take         (B): __ror__ = lambda self, it: it | Slice(self.f) | Pipe(tuple)
class Chunked      (B): __ror__ = lambda self, it: iter(functools.partial(lambda n, i: i | Take(n), self.f, iter(it)), ())
class Sorted       (B): __ror__ = lambda self, it: sorted(it, **self.kw)
class GroupBy      (B): __ror__ = lambda self, it: itertools.groupby(it | Sorted(key=self.f), key=self.f)
class PipeArgs     (B): __ror__ = lambda self, x: self.f(*x)
class StarMap      (B): __ror__ = lambda self, x: x | Map(lambda y: y | PipeArgs(self.f))
class IsUnique     (B): __ror__ = lambda self, seq: len(seq) == len(set(seq if self.f is None else map(self.f, seq)))
class MapApply     (B): __ror__ = lambda self, it: it | Map(lambda x: x | Apply(self.f))
class ReduceByKey  (B): __ror__ = lambda self, it: it | Sorted(lambda kv: kv[0]) | GroupBy(lambda kv: kv[0]) | MapValues(lambda kv: kv | Values() | Reduce(self.f)) | Pipe(list)


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


class Apply(B):
    def __ror__(self, x):
        self.f(x)
        return x


class IterLines(B):
    def __ror__(self, fn):
        with open(fn) as f:
            yield from f
