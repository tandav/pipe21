import functools
import itertools
import operator
import re
import sys

__version__ = '1.23.0'


class B:
    def __init__(self, f=None, *args, **kw):
        self.f = f
        self.args = args
        self.kw = kw


class Pipe         (B): __ror__ = lambda self, x: self.f(x, *self.args, **self.kw)
class Map          (B): __ror__ = lambda self, it: (self.f(x) for x in it)
class Filter       (B): __ror__ = lambda self, it: (x for x in it if self.f(x))
class Reduce       (B): __ror__ = lambda self, it: functools.reduce(self.f, it, *self.args)
class MapKeys      (B): __ror__ = lambda self, it: ((self.f(k), v) for k, v in it)
class MapValues    (B): __ror__ = lambda self, it: ((k, self.f(v)) for k, v in it)
class FilterFalse  (B): __ror__ = lambda self, it: itertools.filterfalse(self.f, it)
class FilterKeys   (B): __ror__ = lambda self, it: (kv for kv in it if (self.f or bool)(kv[0]))
class FilterValues (B): __ror__ = lambda self, it: (kv for kv in it if (self.f or bool)(kv[1]))
class FlatMap      (B): __ror__ = lambda self, it: itertools.chain.from_iterable(self.f(x) for x in it)
class FlatMapValues(B): __ror__ = lambda self, it: ((k, v) for k, vs in it for v in self.f(vs))
class KeyBy        (B): __ror__ = lambda self, it: ((self.f(x), x) for x in it)
class ValueBy      (B): __ror__ = lambda self, it: ((x, self.f(x)) for x in it)
class Append       (B): __ror__ = lambda self, it: ((*x, self.f(x)) for x in it)
class Keys         (B): __ror__ = lambda self, it: (k for k, v in it)
class Values       (B): __ror__ = lambda self, it: (v for k, v in it)
class SwapKV       (B): __ror__ = lambda self, it: it | Map(operator.itemgetter(1, 0))
class Grep         (B): __ror__ = lambda self, it: it | (FilterFalse if self.kw.get('v', False) else Filter)(re.compile(self.f, flags=re.IGNORECASE if self.kw.get('i', False) else 0).search)
class IterLines    (B): __ror__ = lambda self, f: (x.strip() if self.kw.get('strip', True) else x for x in open(f))
class Count        (B): __ror__ = lambda self, it: sum(1 for _ in it)
class Slice        (B): __ror__ = lambda self, it: itertools.islice(it, self.f, *self.args)
class Take         (B): __ror__ = lambda self, it: it | Slice(self.f) | Pipe(list)
class Sorted       (B): __ror__ = lambda self, it: sorted(it, **self.kw)
class GroupBy      (B): __ror__ = lambda self, it: itertools.groupby(sorted(it, key=self.f), key=self.f)
class ReduceByKey  (B): __ror__ = lambda self, it: it | GroupBy(lambda kv: kv[0]) | MapValues(lambda kv: kv | Values() | Reduce(self.f)) | Pipe(list)
class Apply        (B): __ror__ = lambda self, x: x | Exec(self.f, x)
class StarPipe     (B): __ror__ = lambda self, x: self.f(*x)
class StarMap      (B): __ror__ = lambda self, x: itertools.starmap(self.f, x)
class StarFlatMap  (B): __ror__ = lambda self, x: itertools.starmap(self.f, x) | Pipe(itertools.chain.from_iterable)
class MapApply     (B): __ror__ = lambda self, it: (x | Apply(self.f) for x in it)
class Switch       (B): __ror__ = lambda self, x: next((v(x) for k, v in self.f if k(x)), x)
class MapSwitch    (B): __ror__ = lambda self, it: (x | Switch(self.f) for x in it)
class YieldIf      (B): __ror__ = lambda self, it: ((self.f or (lambda y: y))(x) for x in it if self.kw.get('key', bool)(x))
class Join         (B): __ror__ = lambda self, it: it | FlatMap(lambda x: ((x, y) for y in self.f if self.kw.get('key', operator.eq)(x, y)))


class GetItem        (B): __ror__ = lambda self, x: operator.getitem(x, self.f)
class SetItem        (B): __ror__ = lambda self, x: x | Exec(operator.setitem, x, self.f, self.args[0])
class DelItem        (B): __ror__ = lambda self, x: x | Exec(operator.delitem, x, self.f)
class GetAttr        (B): __ror__ = lambda self, x: getattr(x, self.f)
class SetAttr        (B): __ror__ = lambda self, x: x | Exec(setattr, x, self.f, self.args[0])
class DelAttr        (B): __ror__ = lambda self, x: x | Exec(delattr, x, self.f)
class MapGetItem     (B): __ror__ = lambda self, it: (kv | GetItem(self.f) for kv in it)
class MapSetItem     (B): __ror__ = lambda self, it: (kv | SetItem(self.f, self.args[0]) for kv in it)
class MapDelItem     (B): __ror__ = lambda self, it: (kv | DelItem(self.f) for kv in it)
class MapGetAttr     (B): __ror__ = lambda self, it: (kv | GetAttr(self.f) for kv in it)
class MapSetAttr     (B): __ror__ = lambda self, it: (kv | SetAttr(self.f, self.args[0]) for kv in it)
class MapDelAttr     (B): __ror__ = lambda self, it: (kv | DelAttr(self.f) for kv in it)
class MethodCaller   (B): __ror__ = lambda self, x: operator.methodcaller(self.f, *self.args, **self.kw)(x)
class MapMethodCaller(B): __ror__ = lambda self, it: (x | MethodCaller(self.f, *self.args, **self.kw) for x in it)


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


if sys.version_info >= (3, 12):  # pragma: no cover
    class Chunked(B): __ror__ = lambda self, it: itertools.batched(it, self.f)  # pylint: disable=no-member
else:  # pragma: no cover
    class Chunked(B): __ror__ = lambda self, it: iter(functools.partial(lambda n, i: tuple(i | Take(n)), self.f, iter(it)), ())
