import operator
import random

import hypothesis.strategies as st
import pytest
from hypothesis import given

from pipe21 import Append
from pipe21 import Apply
from pipe21 import Chunked
from pipe21 import Count
from pipe21 import Filter
from pipe21 import FilterEqual
from pipe21 import FilterFalse
from pipe21 import FilterKeys
from pipe21 import FilterNotEqual
from pipe21 import FilterValues
from pipe21 import FlatMap
from pipe21 import FlatMapValues
from pipe21 import GroupBy
from pipe21 import IsUnique
from pipe21 import KeyBy
from pipe21 import Keys
from pipe21 import Map
from pipe21 import MapKeys
from pipe21 import MapValues
from pipe21 import Pipe
from pipe21 import PipeArgs
from pipe21 import ReadLines
from pipe21 import Sorted
from pipe21 import Take
from pipe21 import Unique
from pipe21 import ValueBy
from pipe21 import Values


def is_even(x):
    return x % 2 == 0


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_pipe(it):
    assert it | Pipe(list) == list(it)


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_map(it):
    assert it | Map(str) | Pipe(list) == list(map(str, it))


@given(st.lists(st.integers()))
def test_filter(it):
    assert it | Filter(is_even) | Pipe(list) == list(filter(is_even, it))


@given(st.lists(st.integers()))
def test_filter_false(it):
    assert it | FilterFalse(is_even) | Pipe(list) == list(filter(lambda x: not is_even(x), it))


def test_value_by():
    assert range(2) | ValueBy(str) | Pipe(list) == [(0, '0'), (1, '1')]


def test_append():
    assert [(0,), (1,)] | Append(lambda x: str(x[0])) | Pipe(list) == [(0, '0'), (1, '1')]
    assert [(0, '0'), (1, '1')] | Append(lambda x: str(x[0] * 10)) | Pipe(list) == [(0, '0', '0'), (1, '1', '10')]


@pytest.mark.parametrize(
    'seq, key, expected', (
        ([0, 1, 1, 2], None, [0, 1, 2]),
        ('0112', int, ['0', '1', '2']),
        (range(10), lambda x: x % 3, [0, 1, 2]),
        (['a', 'cd', 'cd', 'e', 'fgh'], None, ['a', 'cd', 'e', 'fgh']),
        (['a', 'cd', 'cd', 'e', 'fgh'], len, ['a', 'cd', 'fgh']),
    ),
)
def test_unique(seq, key, expected):
    assert seq | Unique(key) | Pipe(list) == expected


@pytest.mark.parametrize(
    'seq, key, expected', (
        ([0, 1, 2, 3], None, True),
        ([0, 1, 1, 3], None, False),
        ('0123', int, True),
        ('0113', int, False),
    ),
)
def test_is_unique(seq, key, expected):
    assert seq | IsUnique(key) == expected


@pytest.mark.parametrize(
    'it, n, expected', (
        (range(5), 3, (0, 1, 2)),
        (range(5), 1, (0,)),
        (range(5), 0, ()),
        (range(5), 10, (0, 1, 2, 3, 4)),
    ),
)
def test_take(it, n, expected):
    assert it | Take(n) == expected


@pytest.mark.parametrize(
    'it, expected', (
        (range(3), 3),
        (iter(range(3)), 3),
        ('abc', 3),
        ({1, 2, 3}, 3),
        ({'a': 1, 'b': 2}, 2),
    ),
)
def test_count(it, expected):
    assert it | Count() == expected


@pytest.mark.parametrize(
    'it, n, expected', (
        (range(5), 5, [(0, 1, 2, 3, 4)]),
        (range(5), 4, [(0, 1, 2, 3), (4,)]),
        (range(5), 3, [(0, 1, 2), (3, 4)]),
        (range(5), 2, [(0, 1), (2, 3), (4,)]),
        (range(5), 1, [(0,), (1,), (2,), (3,), (4,)]),
        (range(5), 0, []),
    ),
)
def test_chunked(it, n, expected):
    assert it | Chunked(n) | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, kw', (
        ([3, 5, 1, 0], {}),
        ([3, 5, 1, 0], {'reverse': True}),
        ('3510', {'key': int}),
        ('3510', {'key': int, 'reverse': True}),
        ('9j8xy2m#98g%^xd$', {'key': ord, 'reverse': True}),
        ('9j8xy2m#98g%^xd$', {'key': ord, 'reverse': False}),
    ),
)
def test_sorted(it, kw):
    assert it | Sorted(**kw) == sorted(it, **kw)


@pytest.mark.parametrize(
    'it, f ,expected', (
        ([0, 2, 3, 0, 4], range, [0, 1, 0, 1, 2, 0, 1, 2, 3]),
        ([2, 3, 4], lambda x: [(x, x), (x, x)], [(2, 2), (2, 2), (3, 3), (3, 3), (4, 4), (4, 4)]),
    ),
)
def test_flat_map(it, f, expected):
    assert it | FlatMap(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, f ,expected', (
        ([('a', ['x', 'y', 'z']), ('b', ['p', 'r'])], lambda x: x, [('a', 'x'), ('a', 'y'), ('a', 'z'), ('b', 'p'), ('b', 'r')]),
    ),
)
def test_flat_map_values(it, f, expected):
    assert it | FlatMapValues(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, f ,expected', (
        ([(0, 2), (3, 0)], None, [(3, 0)]),
        ([(0, 2), (3, 0)], lambda x: x % 2 == 0, [(0, 2)]),
    ),
)
def test_filter_keys(it, f ,expected):
    assert it | FilterKeys(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, f ,expected', (
        ([(0, 2), (3, 0)], None, [(0, 2)]),
        ([(0, 2), (3, 0)], lambda x: x % 2 == 0, [(0, 2), (3, 0)]),
    ),
)
def test_filter_values(it, f ,expected):
    assert it | FilterValues(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, f, expected', [
        ([(0, 'a'), (0, 'b'), (1, 'c'), (2, 'd')], operator.itemgetter(0), [(0, [(0, 'a'), (0, 'b')]), (1, [(1, 'c')]), (2, [(2, 'd')])]),
        (['ab', 'cd', 'e', 'f', 'gh', 'ij'], len, [(2, ['ab', 'cd']), (1, ['e', 'f']), (2, ['gh', 'ij'])]),
    ],
)
def test_groupby(it, f, expected):
    assert it | GroupBy(f) | MapValues(list) | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, f, expected', [
        ((1, 2), operator.add, 3),
        (('FF', 16), int, 255),
        (([1, 2], 'A'), dict.fromkeys, {1: 'A', 2: 'A'}),
        (({1, 2}, {3, 4, 5}), set.union, {1, 2, 3, 4, 5}),
    ],
)
def test_pipe_args(it, f, expected):
    assert it | PipeArgs(f) == expected


@pytest.mark.parametrize(
    'it, expected', [
        ([(0, 'a'), (1, 'b')], [0, 1]),
    ],
)
def test_keys(it, expected):
    assert it | Keys() | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, expected', [
        ([(0, 'a'), (1, 'b')], ['a', 'b']),
    ],
)
def test_values(it, expected):
    assert it | Values() | Pipe(list) == expected


def test_map_keys_map_values():
    assert [(1, 10), (2, 20)] | MapKeys(str) | Pipe(list) == [('1', 10), ('2', 20)]
    assert [(1, 10), (2, 20)] | MapValues(str) | Pipe(list) == [(1, '10'), (2, '20')]


def test_key_by_value_by():
    assert range(2) | KeyBy(str) | Pipe(list) == [('0', 0), ('1', 1)]
    assert range(2) | ValueBy(str) | Pipe(list) == [(0, '0'), (1, '1')]


def test_apply():
    random.seed(42)
    assert range(5) | Pipe(list) | Apply(random.shuffle) == [3, 1, 2, 4, 0]


def test_read_lines():
    assert 'tests/testing/file.txt' | ReadLines() == ['hello', 'world']


def test_filter_equal():
    assert range(3) | FilterEqual(2) | Pipe(list) == [2]


def test_filter_not_equal():
    assert range(3) | FilterNotEqual(2) | Pipe(list) == [0, 1]
