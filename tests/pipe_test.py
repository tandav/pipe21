import functools
import operator
import random

import hypothesis.strategies as st
import pytest
from hypothesis import given

from pipe21 import *


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


@pytest.mark.parametrize(
    'it, initializer', [
        ([], 0),
        ([], None),
        ([1, 2, 3], 0),
        ([1, 2, 3], 1),
        ([1, 2, 3], None),
        (range(0), 0),
        (range(10), 0),
        (range(10), 1),
        (range(10), None),
        (list('abc'), ''),
        (list('abc'), 'd'),
        (list('abc'), None),
        (list(''), ''),
        (list(''), 'd'),
        (list(''), None),
    ],
)
def test_reduce(it, initializer):
    if len(it) == 0 and initializer is None:
        with pytest.raises(TypeError):
            it | Reduce(operator.add)  # pylint: disable=W0106
        return

    if initializer is None:
        assert it | Reduce(operator.add) == functools.reduce(operator.add, it)
        return
    assert it | Reduce(operator.add, initializer) == functools.reduce(operator.add, it, initializer)


@given(st.lists(st.integers()))
def test_filter_false(it):
    assert it | FilterFalse(is_even) | Pipe(list) == list(filter(lambda x: not is_even(x), it))


def test_value_by():
    assert range(2) | ValueBy(str) | Pipe(list) == [(0, '0'), (1, '1')]


@pytest.mark.parametrize(
    'it, f ,expected', (
        ([(0,), (1,)], lambda x: str(x[0]), [(0, '0'), (1, '1')]),
        ([(0, '0'), (1, '1')], lambda x: str(x[0] * 10), [(0, '0', '0'), (1, '1', '10')]),
    ),
)
def test_append(it, f ,expected):
    assert it | Append(f) | Pipe(list) == expected
    assert it | Append(f) | Pipe(list) == expected


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
    'it, args, expected', (
        (range(5), (2,), [0, 1]),
        (range(5), (2, 4), [2, 3]),
        (range(5), (2, None), [2, 3, 4]),
        (range(5), (0, None, 2), [0, 2, 4]),
    ),
)
def test_slice(it, args, expected):
    assert it | Slice(*args) | Pipe(list) == expected

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
        ([('a', 1), ('b', 1), ('a', 1)], operator.add, [('a', 2), ('b', 1)]),
    ],
)
def test_reduce_by_key(it, f, expected):
    assert it | ReduceByKey(f) == expected


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
    'it, f, expected', [
        ([(2, 5), (3, 2), (10, 3)], pow, [32, 9, 1000]),
        ([('00', 16), ('A5', 16), ('FF', 16)], int, [0, 165, 255]),
    ],
)
def test_map_args(it, f, expected):
    assert it | StarMap(f) | Pipe(list) == expected


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


@pytest.mark.parametrize(
    'it, grep, expected', [
        (['hello 42 bro', 'world', 'awesome 42'], '42', ['hello 42 bro', 'awesome 42']),
        (['foo1', 'foo2', '3foo', 'bar1'], '^foo.*', ['foo1', 'foo2']),
    ],
)
def test_grep(it, grep, expected):
    assert it | Grep(grep) | Pipe(list) == expected


@pytest.mark.parametrize(
    'it, grep, expected', [
        (['hello 42 bro', 'world', 'awesome 42'], '42', ['world']),
        (['foo1', 'foo2', '3foo', 'bar1'], '^foo.*', ['3foo', 'bar1']),
    ],
)
def test_grep_v(it, grep, expected):
    assert it | GrepV(grep) | Pipe(list) == expected


def test_apply():
    random.seed(42)
    assert range(5) | Pipe(list) | Apply(random.shuffle) == [3, 1, 2, 4, 0]


def test_apply_map():
    random.seed(42)
    assert range(3, 5) | Map(range) | Map(list) | MapApply(random.shuffle) | Pipe(list) == [[1, 0, 2], [3, 1, 2, 0]]


def test_iter_lines(tmp_path):
    file = tmp_path / 'file.txt'
    file.write_text('hello\nworld\n')
    assert file | IterLines() | Pipe(list) == ['hello\n', 'world\n']
