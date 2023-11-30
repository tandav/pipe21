import functools
import itertools
import operator
import re

__version__ = '1.22.0'


class B:
    def __init__(self, f=None, *args, **kw):
        self.f = f
        self.args = args
        self.kw = kw


class Pipe         (B): __ror__ = lambda self, x: self.f(x, *self.args, **self.kw)
class Map          (B): __ror__ = lambda self, it: map(self.f, it)
class Filter       (B): __ror__ = lambda self, it: filter(self.f, it)
class Reduce       (B): __ror__ = lambda self, it: functools.reduce(self.f, it, *self.args)
class MapKeys      (B): __ror__ = lambda self, it: it | Map(lambda kv: (self.f(kv[0]), kv[1]))
class MapValues    (B): __ror__ = lambda self, it: it | Map(lambda kv: (kv[0], self.f(kv[1])))
class FilterFalse  (B): __ror__ = lambda self, it: itertools.filterfalse(self.f, it)
class FilterKeys   (B): __ror__ = lambda self, it: it | Filter(lambda kv: kv[0] | Pipe(self.f or bool))
class FilterValues (B): __ror__ = lambda self, it: it | Filter(lambda kv: kv[1] | Pipe(self.f or bool))
class FlatMap      (B): __ror__ = lambda self, it: it | Map(self.f) | Pipe(itertools.chain.from_iterable)
class FlatMapValues(B): __ror__ = lambda self, it: it | FlatMap(lambda kv: ((kv[0], x) for x in self.f(kv[1])))
class KeyBy        (B): __ror__ = lambda self, it: it | Map(lambda x: (self.f(x), x))
class ValueBy      (B): __ror__ = lambda self, it: it | Map(lambda x: (x, self.f(x)))
class Append       (B): __ror__ = lambda self, it: it | Map(lambda x: (*x, self.f(x)))
class Keys         (B): __ror__ = lambda self, it: it | Map(lambda kv: kv[0])
class Values       (B): __ror__ = lambda self, it: it | Map(lambda kv: kv[1])
class Grep         (B): __ror__ = lambda self, it: it | (FilterFalse if self.kw.get('v', False) else Filter)(re.compile(self.f, flags=re.I if self.kw.get('i', False) else 0).search)
class IterLines    (B): __ror__ = lambda self, p: p | Pipe(open) | Pipe(lambda t: t | Map(str.strip) if self.kw.get('strip', True) else t)
class Count        (B): __ror__ = lambda self, it: sum(1 for _ in it)
class Slice        (B): __ror__ = lambda self, it: itertools.islice(it, self.f, *self.args)
class Take         (B): __ror__ = lambda self, it: it | Slice(self.f) | Pipe(tuple)
class Chunked      (B): __ror__ = lambda self, it: iter(functools.partial(lambda n, i: i | Take(n), self.f, iter(it)), ())
class Sorted       (B): __ror__ = lambda self, it: sorted(it, **self.kw)
class GroupBy      (B): __ror__ = lambda self, it: it | Sorted(key=self.f) | Pipe(itertools.groupby, key=self.f)
class ReduceByKey  (B): __ror__ = lambda self, it: it | GroupBy(lambda kv: kv[0]) | MapValues(lambda kv: kv | Values() | Reduce(self.f)) | Pipe(list)
class Apply        (B): __ror__ = lambda self, x: x | Exec(self.f, x)
class StarPipe     (B): __ror__ = lambda self, x: self.f(*x)
class StarMap      (B): __ror__ = lambda self, x: itertools.starmap(self.f, x)
class StarFlatMap  (B): __ror__ = lambda self, x: x | StarMap(self.f) | Pipe(itertools.chain.from_iterable)
class MapApply     (B): __ror__ = lambda self, it: it | Map(lambda x: x | Apply(self.f))
class Switch       (B): __ror__ = lambda self, x: self.f | FilterKeys(lambda p: p(x)) | Values() | Map(lambda f: f(x)) | Pipe(next, x)
class MapSwitch    (B): __ror__ = lambda self, it: it | Map(lambda x: x | Switch(self.f))
class YieldIf      (B): __ror__ = lambda self, it: ((self.f or (lambda y: y))(x) for x in it if self.kw.get('key', bool)(x))
class Join         (B): __ror__ = lambda self, it: it | FlatMap(lambda x: ((x, y) for y in self.f if self.kw.get('key', operator.eq)(x, y)))


class GetItem        (B): __ror__ = lambda self, x: operator.getitem(x, self.f)
class SetItem        (B): __ror__ = lambda self, x: x | Exec(operator.setitem, x, self.f, self.args[0])
class DelItem        (B): __ror__ = lambda self, x: x | Exec(operator.delitem, x, self.f)
class GetAttr        (B): __ror__ = lambda self, x: getattr(x, self.f)
class SetAttr        (B): __ror__ = lambda self, x: x | Exec(setattr, x, self.f, self.args[0])
class DelAttr        (B): __ror__ = lambda self, x: x | Exec(delattr, x, self.f)
class MapGetItem     (B): __ror__ = lambda self, it: it | Map(lambda kv: kv | GetItem(self.f))
class MapSetItem     (B): __ror__ = lambda self, it: it | Map(lambda kv: kv | SetItem(self.f, self.args[0]))
class MapDelItem     (B): __ror__ = lambda self, it: it | Map(lambda kv: kv | DelItem(self.f))
class MapGetAttr     (B): __ror__ = lambda self, it: it | Map(lambda kv: kv | GetAttr(self.f))
class MapSetAttr     (B): __ror__ = lambda self, it: it | Map(lambda kv: kv | SetAttr(self.f, self.args[0]))
class MapDelAttr     (B): __ror__ = lambda self, it: it | Map(lambda kv: kv | DelAttr(self.f))
class MethodCaller   (B): __ror__ = lambda self, x: operator.methodcaller(self.f, *self.args, **self.kw)(x)
class MapMethodCaller(B): __ror__ = lambda self, it: it | Map(lambda x: x | MethodCaller(self.f, *self.args, **self.kw))


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


class Exec(B):
    def __ror__(self, x):
        self.f(*self.args, **self.kw)
        return x
