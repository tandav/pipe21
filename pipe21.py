import functools
import itertools
import re

__version__ = '1.8.0'


class B:
    def __init__(self, op):
        self.op = op

    def __call__(self, f=None, *args, **kw):
        self.f = f  # pylint: disable=attribute-defined-outside-init
        self.args = args  # pylint: disable=attribute-defined-outside-init
        self.kw = kw  # pylint: disable=attribute-defined-outside-init
        return self

    def __ror__(self, other):
        return self.op(self, other)


Pipe = B(lambda self, x: self.f(x))
Map = B(lambda self, x: map(self.f, x))
Filter = B(lambda self, x: filter(self.f, x))

Reduce = B(lambda self, x: functools.reduce(self.f, x, *self.args))
MapValues = B(lambda self, x: x | Map(lambda kv: (kv[0], self.f(kv[1]))))
MapKeys = B(lambda self, x: x | Map(lambda kv: (self.f(kv[0]), kv[1])))
FilterFalse = B(lambda self, x: x | Filter(lambda x: not self.f(x)))
FilterKeys = B(lambda self, x: x | Filter(lambda x: (self.f or bool)(x[0])))
FilterValues = B(lambda self, x: x | Filter(lambda x: (self.f or bool)(x[1])))
FlatMap = B(lambda self, x: x | Map(self.f) | Pipe(itertools.chain.from_iterable))
FlatMapValues = B(lambda self, x: x | FlatMap(lambda kv: ((kv[0], y) for y in self.f(kv[1]))))
KeyBy = B(lambda self, x: x | Map(lambda x: (self.f(x), x)))
ValueBy = B(lambda self, x: x | Map(lambda x: (x, self.f(x))))
Append = B(lambda self, x: x | Map(lambda x: (*x, self.f(x))))
Keys = B(lambda self, x: x | Map(lambda x: x[0]))
Values = B(lambda self, x: x | Map(lambda x: x[1]))
Grep = B(lambda self, x: x | Filter(lambda x: re.search(self.f, x)))
GrepV = B(lambda self, x: x | Filter(lambda x: not re.search(self.f, x)))
Count = B(lambda self, x: sum(1 for _ in x))
Slice = B(lambda self, x: itertools.islice(x, self.f, *self.args))
Take = B(lambda self, x: x | Slice(self.f) | Pipe(tuple))
Chunked = B(lambda self, x: iter(functools.partial(lambda n, i: i | Take(n), self.f, iter(x)), ()))
GroupBy = B(lambda self, x: itertools.groupby(x, key=self.f))
PipeArgs = B(lambda self, x: self.f(*x))
StarMap = B(lambda self, x: x | Map(lambda y: y | PipeArgs(self.f)))
IsUnique = B(lambda self, x: len(set(x)) == len(x))
Sorted = B(lambda self, x: sorted(x, **self.kw))
MapApply = B(lambda self, x: x | Map(lambda y: y | Apply(self.f)))
ReduceByKey = B(lambda self, x: x | Sorted(lambda kv: kv[0]) | GroupBy(lambda kv: kv[0]) | MapValues(lambda kv: kv | Values() | Reduce(self.f)) | Pipe(list))


def unique(self, it):
    key = self.f or (lambda x: x)
    seen = set()
    for item in it:
        k = key(item)
        if k in seen:
            continue
        seen.add(k)
        yield item


Unique = B(unique)


def apply(self, x):
    self.f(x)
    return x


Apply = B(apply)


def iter_lines(self, fn):  # pylint: disable=W0613
    with open(fn) as f:
        yield from f


IterLines = B(iter_lines)
