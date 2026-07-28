"""Laziness contract: streaming operators must not consume the source until pulled."""
import itertools
import operator
from types import SimpleNamespace

import pytest

from pipe21 import *


class Source:
    """An unbounded iterable that records how many items were pulled from it."""

    def __init__(self, item=lambda i: i):
        self.item = item
        self.consumed = 0

    def __iter__(self):
        for i in itertools.count():
            self.consumed += 1
            yield self.item(i)


def kv(i):
    return i, [i]


def dct(i):
    return {'a': i}


def ns(i):
    return SimpleNamespace(a=i)


lazy_ops = [
    (Map(str), int),
    (Filter(lambda x: True), int),
    (FilterFalse(lambda x: False), int),
    (FlatMap(lambda x: [x]), int),
    (KeyBy(str), int),
    (ValueBy(str), int),
    (Unique(), int),
    (MapApply(lambda x: None), int),
    (Slice(None), int),
    (Slice(0, None, 2), int),
    (Chunked(2), int),
    (Join([0, 1, 2]), int),
    (YieldIf(str), int),
    (MapSwitch([(lambda x: True, str)]), int),
    (MapKeys(str), kv),
    (MapValues(str), kv),
    (FilterKeys(lambda x: True), kv),
    (FilterValues(lambda x: True), kv),
    (FlatMapValues(lambda vs: vs), kv),
    (Keys(), kv),
    (Values(), kv),
    (SwapKV(), kv),
    (Append(lambda x: str(x[0])), lambda i: (i,)),
    (StarMap(operator.add), lambda i: (i, i)),
    (StarFlatMap(lambda a, b: [(a, b)]), lambda i: (i, i)),
    (Grep(r'\d'), str),
    (MapMethodCaller('upper'), str),
    (MapGetItem('a'), dct),
    (MapSetItem('b', 1), dct),
    (MapDelItem('a'), dct),
    (MapGetAttr('a'), ns),
    (MapSetAttr('b', 1), ns),
    (MapDelAttr('a'), ns),
]
lazy_ids = [type(op).__name__ for op, _ in lazy_ops]


@pytest.mark.parametrize(('op', 'item'), lazy_ops, ids=lazy_ids)
def test_lazy_does_not_consume_on_construction(op, item):
    source = Source(item)
    source | op  # pylint: disable=W0104,W0106
    assert source.consumed == 0


@pytest.mark.parametrize(('op', 'item'), lazy_ops, ids=lazy_ids)
def test_lazy_streams_from_infinite_source(op, item):
    source = Source(item)
    assert len(source | op | Take(3)) == 3
    assert source.consumed < 100, 'operator over-consumed an unbounded source'


eager_ops = [
    Pipe(list),
    Take(10),
    Count(),
    Sorted(),
    Reduce(operator.add),
    GroupBy(str),
]


@pytest.mark.parametrize('op', eager_ops, ids=[type(op).__name__ for op in eager_ops])
def test_eager_consumes_whole_source(op):
    source = Source()
    it = itertools.islice(iter(source), 10)
    it | op  # pylint: disable=W0104,W0106
    assert source.consumed == 10


def test_chained_pipeline_is_lazy_end_to_end():
    source = Source()
    pipe = source | Map(lambda x: x * 2) | Filter(lambda x: x % 3 == 0) | Unique() | Chunked(2)
    assert source.consumed == 0
    assert pipe | Take(2) == [(0, 6), (12, 18)]
    assert source.consumed == 10


def test_lazy_operators_do_not_re_read_source():
    """A one-shot iterator is consumed exactly once by a chain of streaming operators."""
    it = iter([1, 2, 3, 4])
    assert it | Map(str) | Filter(lambda x: x != '2') | Pipe(list) == ['1', '3', '4']
    assert next(it, None) is None
