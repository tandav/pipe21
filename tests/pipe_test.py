import functools
import itertools
import math
import operator
import random
from types import SimpleNamespace

import hypothesis.strategies as st
import pytest
from hypothesis import given

from pipe21 import *


def is_even(x):
    return x % 2 == 0


def yield_even(it):
    for x in it:
        if x % 2 == 0:
            yield x


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_pipe(it):
    assert it | Pipe(list) == list(it)


def test_pipe_args_kwargs():
    assert 2 | Pipe(pow, 8) == 256
    assert 'FF' | Pipe(int, base=16) == 255
    assert b'\x02\x00' | Pipe(int.from_bytes, byteorder='big') == 512
    assert 'ab' | Pipe(enumerate, start=0) | Pipe(list) == [(0, 'a'), (1, 'b')]
    assert 5.01 | Pipe(math.isclose, 5, abs_tol=0.01) is True
    random.seed(44)
    assert [0, 1, 2] | Pipe(random.choices, [0.8, 0.15, 0.05], k=20) == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    assert [0, 1, 2] | Pipe(itertools.zip_longest, 'ab', fillvalue=None) | Pipe(list) == [(0, 'a'), (1, 'b'), (2, None)]
    assert [0, 1, 2] | Pipe(itertools.accumulate, operator.add, initial=100) | Pipe(list) == [100, 100, 101, 103]


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_map(it):
    assert it | Map(str) | Pipe(list) == list(map(str, it))


@given(st.lists(st.integers()))
def test_filter(it):
    assert it | Filter(is_even) | Pipe(list) == list(filter(is_even, it))


@pytest.mark.parametrize(
    ('it', 'f', 'initializer'), [
        ([], operator.add, 0),
        ([], operator.add, None),
        ([1, 2, 3], operator.add, 0),
        ([1, 2, 3], operator.add, 1),
        ([1, 2, 3], operator.add, None),
        (range(0), operator.add, 0),
        (range(10), operator.add, 0),
        (range(10), operator.add, 1),
        (range(10), operator.add, None),
        (list('abc'), operator.add, ''),
        (list('abc'), operator.add, 'd'),
        (list('abc'), operator.add, None),
        (list(''), operator.add, ''),
        (list(''), operator.add, 'd'),
        (list(''), operator.add, None),
        ([{1, 2}, {3, 4, 5}, {4, 5}], operator.or_, {1, 2, 3, 4, 5}),
    ],
)
def test_reduce(it, f, initializer):
    if len(it) == 0 and initializer is None:
        with pytest.raises(TypeError):
            it | Reduce(f)  # pylint: disable=W0106
        return

    if initializer is None:
        assert it | Reduce(f) == functools.reduce(f, it)
        return
    assert it | Reduce(f, initializer) == functools.reduce(f, it, initializer)


def test_map_keys_map_values():
    assert [(1, 10), (2, 20)] | MapKeys(str) | Pipe(list) == [('1', 10), ('2', 20)]
    assert [(1, 10), (2, 20)] | MapValues(str) | Pipe(list) == [(1, '10'), (2, '20')]


@given(st.lists(st.integers()))
def test_filter_false(it):
    assert it | FilterFalse(is_even) | Pipe(list) == list(filter(lambda x: not is_even(x), it))


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([(0, 2), (3, 0)], None, [(3, 0)]),
        ([(0, 2), (3, 0)], lambda x: x % 2 == 0, [(0, 2)]),
    ],
)
def test_filter_keys(it, f, expected):
    assert it | FilterKeys(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([(0, 2), (3, 0)], None, [(0, 2)]),
        ([(0, 2), (3, 0)], lambda x: x % 2 == 0, [(0, 2), (3, 0)]),
    ],
)
def test_filter_values(it, f, expected):
    assert it | FilterValues(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([0, 2, 3, 0, 4], range, [0, 1, 0, 1, 2, 0, 1, 2, 3]),
        ([2, 3, 4], lambda x: [(x, x), (x, x)], [(2, 2), (2, 2), (3, 3), (3, 3), (4, 4), (4, 4)]),
        ([range(0, 5), range(100, 105)], yield_even, [0, 2, 4, 100, 102, 104]),
        ([range(0, 5), range(100, 105)], lambda it: (x for x in it if x % 2 == 0), [0, 2, 4, 100, 102, 104]),
    ],
)
def test_flat_map(it, f, expected):
    assert it | FlatMap(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([('a', ['x', 'y', 'z']), ('b', ['p', 'r'])], lambda x: x, [('a', 'x'), ('a', 'y'), ('a', 'z'), ('b', 'p'), ('b', 'r')]),
        ([('a', [0, 1, 2]), ('b', [3, 4])], yield_even, [('a', 0), ('a', 2), ('b', 4)]),
    ],
)
def test_flat_map_values(it, f, expected):
    assert it | FlatMapValues(f) | Pipe(list) == expected


def test_key_by_value_by():
    assert range(2) | KeyBy(str) | Pipe(list) == [('0', 0), ('1', 1)]
    assert range(2) | ValueBy(str) | Pipe(list) == [(0, '0'), (1, '1')]


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([(0,), (1,)], lambda x: str(x[0]), [(0, '0'), (1, '1')]),
        ([(0, '0'), (1, '1')], lambda x: str(x[0] * 10), [(0, '0', '0'), (1, '1', '10')]),
    ],
)
def test_append(it, f, expected):
    assert it | Append(f) | Pipe(list) == expected
    assert it | Append(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'expected'), [
        ([(0, 'a'), (1, 'b')], [0, 1]),
    ],
)
def test_keys(it, expected):
    assert it | Keys() | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'expected'), [
        ([(0, 'a'), (1, 'b')], ['a', 'b']),
    ],
)
def test_values(it, expected):
    assert it | Values() | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'grep', 'expected'), [
        (['hello foo', 'world', 'awesome FOo'], 'foo', ['hello foo']),
        (['foo1', 'foo2', '3foo', 'bar1'], '^foo.*', ['foo1', 'foo2']),
    ],
)
def test_grep(it, grep, expected):
    assert it | Grep(grep) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'grep', 'expected'), [
        (['hello foo', 'world', 'awesome FOo'], 'foo', ['world', 'awesome FOo']),
        (['foo1', 'foo2', '3foo', 'bar1'], '^foo.*', ['3foo', 'bar1']),
    ],
)
def test_grep_v(it, grep, expected):
    assert it | Grep(grep, v=True) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'grep', 'v', 'i', 'expected'), [
        (['hello foo', 'world', 'awesome FOo'], 'foo', False, False, ['hello foo']),
        (['hello foo', 'world', 'awesome FOo'], 'foo', False, True, ['hello foo', 'awesome FOo']),
        (['hello foo', 'world', 'awesome FOo'], 'Foo', False, True, ['hello foo', 'awesome FOo']),
        (['hello foo', 'world', 'awesome FOo'], 'foo', True, False, ['world', 'awesome FOo']),
        (['hello foo', 'world', 'awesome FOo'], 'foo', True, True, ['world']),
        (['hello foo', 'world', 'awesome FOo'], 'Foo', True, True, ['world']),
    ],
)
def test_grep_i(it, v, grep, i, expected):
    assert it | Grep(grep, v=v, i=i) | Pipe(list) == expected


def test_iter_lines(tmp_path):
    file = tmp_path / 'file.txt'
    file.write_text('hello\nworld\n')
    assert file | IterLines() | Pipe(list) == ['hello', 'world']
    assert file | IterLines(strip=False) | Pipe(list) == ['hello\n', 'world\n']


@pytest.mark.parametrize(
    ('it', 'expected'), [
        (range(3), 3),
        (iter(range(3)), 3),
        ('abc', 3),
        ({1, 2, 3}, 3),
        ({'a': 1, 'b': 2}, 2),
    ],
)
def test_count(it, expected):
    assert it | Count() == expected


@pytest.mark.parametrize(
    ('it', 'args', 'expected'), [
        (range(5), (2,), [0, 1]),
        (range(5), (2, 4), [2, 3]),
        (range(5), (2, None), [2, 3, 4]),
        (range(5), (0, None, 2), [0, 2, 4]),
    ],
)
def test_slice(it, args, expected):
    assert it | Slice(*args) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'n', 'expected'), [
        (range(5), 3, [0, 1, 2]),
        (range(5), 1, [0]),
        (range(5), 0, []),
        (range(5), 10, [0, 1, 2, 3, 4]),
    ],
)
def test_take(it, n, expected):
    assert it | Take(n) == expected


@pytest.mark.parametrize(
    ('it', 'n', 'expected'), [
        (range(5), 5, [(0, 1, 2, 3, 4)]),
        (range(5), 4, [(0, 1, 2, 3), (4,)]),
        (range(5), 3, [(0, 1, 2), (3, 4)]),
        (range(5), 2, [(0, 1), (2, 3), (4,)]),
        (range(5), 1, [(0,), (1,), (2,), (3,), (4,)]),
    ],
)
def test_chunked(it, n, expected):
    assert it | Chunked(n) | Pipe(list) == expected


@pytest.mark.skipif(sys.version_info >= (3, 12), reason='pre itertools.batched implementation for python<3.12')
def test_chunked_zero_without_itertools_batched():
    assert range(5) | Chunked(0) | Pipe(list) == []


@pytest.mark.skipif(sys.version_info < (3, 12), reason='itertools.batched implementation for python>=3.12')
def test_chunked_zero_itertools_batched():
    with pytest.raises(ValueError, match='n must be at least one'):
        assert range(5) | Chunked(0) | Pipe(list) == []


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([(0, 'a'), (1, 'c'), (0, 'b'), (2, 'd')], operator.itemgetter(0), [(0, [(0, 'a'), (0, 'b')]), (1, [(1, 'c')]), (2, [(2, 'd')])]),
        (['ab', 'cd', 'e', 'f', 'gh', 'ij'], len, [(1, ['e', 'f']), (2, ['ab', 'cd', 'gh', 'ij'])]),
    ],
)
def test_groupby(it, f, expected):
    assert it | GroupBy(f) | MapValues(list) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ((1, 2), operator.add, 3),
        (('FF', 16), int, 255),
        (([1, 2], 'A'), dict.fromkeys, {1: 'A', 2: 'A'}),
        (({1, 2}, {3, 4, 5}), set.union, {1, 2, 3, 4, 5}),
    ],
)
def test_star_pipe(it, f, expected):
    assert it | StarPipe(f) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([(2, 5), (3, 2), (10, 3)], pow, [32, 9, 1000]),
        ([('00', 16), ('A5', 16), ('FF', 16)], int, [0, 165, 255]),
    ],
)
def test_star_map(it, f, expected):
    assert it | StarMap(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        (range(2, 10) | Pipe(itertools.permutations, r=2), lambda a, b: [(a, b)] if a % b == 0 else [], [(4, 2), (6, 2), (6, 3), (8, 2), (8, 4), (9, 3)]),
    ],
)
def test_star_flatmap(it, f, expected):
    assert it | StarFlatMap(f) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'kw'), [
        ([3, 5, 1, 0], {}),
        ([3, 5, 1, 0], {'reverse': True}),
        ('3510', {'key': int}),
        ('3510', {'key': int, 'reverse': True}),
        ('9j8xy2m#98g%^xd$', {'key': ord, 'reverse': True}),
        ('9j8xy2m#98g%^xd$', {'key': ord, 'reverse': False}),
    ],
)
def test_sorted(it, kw):
    assert it | Sorted(**kw) == sorted(it, **kw)


def test_map_apply():
    random.seed(42)
    assert range(3, 5) | Map(range) | Map(list) | MapApply(random.shuffle) | Pipe(list) == [[1, 0, 2], [3, 1, 2, 0]]


cases = [
    (lambda i: i % 3 == i % 5 == 0, lambda x: 'FizzBuzz'),
    (lambda i: i % 3 == 0, lambda x: 'Fizz'),
    (lambda i: i % 5 == 0, lambda x: 'Buzz'),
    (lambda i: i > 100, lambda x: f'{x} is large'),
]


@pytest.mark.parametrize(
    ('x', 'expected'), [
        (1, 1),
        (3, 'Fizz'),
        (5, 'Buzz'),
        (15, 'FizzBuzz'),
        (101, '101 is large'),
    ],
)
def test_switch(x, expected):
    assert x | Switch(cases) == expected


@pytest.mark.parametrize(
    ('it', 'cases', 'expected'), [
        (range(1, 100), cases, [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17, 'Fizz', 19, 'Buzz', 'Fizz', 22, 23, 'Fizz', 'Buzz', 26, 'Fizz', 28, 29, 'FizzBuzz', 31, 32, 'Fizz', 34, 'Buzz', 'Fizz', 37, 38, 'Fizz', 'Buzz', 41, 'Fizz', 43, 44, 'FizzBuzz', 46, 47, 'Fizz', 49, 'Buzz', 'Fizz', 52, 53, 'Fizz', 'Buzz', 56, 'Fizz', 58, 59, 'FizzBuzz', 61, 62, 'Fizz', 64, 'Buzz', 'Fizz', 67, 68, 'Fizz', 'Buzz', 71, 'Fizz', 73, 74, 'FizzBuzz', 76, 77, 'Fizz', 79, 'Buzz', 'Fizz', 82, 83, 'Fizz', 'Buzz', 86, 'Fizz', 88, 89, 'FizzBuzz', 91, 92, 'Fizz', 94, 'Buzz', 'Fizz', 97, 98, 'Fizz']),
        (range(5), [(lambda x: x % 2 == 0, lambda x: x * 100)], [0, 1, 200, 3, 400]),
    ],
)
def test_map_switch(it, cases, expected):
    assert it | MapSwitch(cases) | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'key', 'expected'), [
        (range(5), lambda x: x * 100, None, [100, 200, 300, 400]),
        (range(5), lambda x: x * 100, lambda x: x % 2 == 0, [0, 200, 400]), (range(5), None, None, [1, 2, 3, 4]),
        (range(5), None, lambda x: x % 2 == 0, [0, 2, 4]),
        (range(5), None, None, [1, 2, 3, 4]),
    ],
)
def test_yield_if(it, f, key, expected):
    y = YieldIf(f) if key is None else YieldIf(f, key=key)
    assert it | y | Pipe(list) == expected


@pytest.mark.parametrize(
    ('a', 'b', 'key', 'expected'), [
        (range(5), range(2, 5), None, [(2, 2), (3, 3), (4, 4)]),
        (range(1, 7), range(2, 6), lambda x, y: x % y == 0, [(2, 2), (3, 3), (4, 2), (4, 4), (5, 5), (6, 2), (6, 3)]),
    ],
)
def test_join(a, b, key, expected):
    j = Join(b) if key is None else Join(b, key=key)
    assert a | j | Pipe(list) == expected


@pytest.mark.parametrize(
    ('it', 'f', 'expected'), [
        ([('a', 1), ('b', 1), ('a', 1)], operator.add, [('a', 2), ('b', 1)]),
    ],
)
def test_reduce_by_key(it, f, expected):
    assert it | ReduceByKey(f) == expected


def test_apply():
    random.seed(42)
    assert range(5) | Pipe(list) | Apply(random.shuffle) == [3, 1, 2, 4, 0]


def test_descriptors():
    assert {'a': 'b'} | GetItem('a') == 'b'
    assert {'a': 'b'} | SetItem('foo', 'bar') == {'a': 'b', 'foo': 'bar'}
    assert {'a': 'b'} | DelItem('a') == {}
    assert [{'a': 'b'}] | MapGetItem('a') | Pipe(list) == ['b']
    assert [{'a': 'b'}] | MapSetItem('foo', 'bar') | Pipe(list) == [{'a': 'b', 'foo': 'bar'}]
    assert [{'a': 'b'}] | MapDelItem('a') | Pipe(list) == [{}]
    assert SimpleNamespace(a='b') | GetAttr('a') == 'b'
    assert SimpleNamespace(a='b') | SetAttr('foo', 'bar') == SimpleNamespace(a='b', foo='bar')
    assert SimpleNamespace(a='b') | DelAttr('a') == SimpleNamespace()
    assert [SimpleNamespace(a='b')] | MapGetAttr('a') | Pipe(list) == ['b']
    assert [SimpleNamespace(a='b')] | MapSetAttr('foo', 'bar') | Pipe(list) == [SimpleNamespace(a='b', foo='bar')]
    assert [SimpleNamespace(a='b')] | MapDelAttr('a') | Pipe(list) == [SimpleNamespace()]


class K:
    def hello(self):
        return 'hello'

    def increment(self, i, add=1):
        return i + add


def test_methodcaller():
    k = K()
    assert k | MethodCaller('hello') == 'hello'
    assert k | MethodCaller('increment', 1) == 2
    assert k | MethodCaller('increment', 1, add=2) == 3
    assert [k] | MapMethodCaller('hello') | Pipe(list) == ['hello']


@pytest.mark.parametrize(
    ('seq', 'key', 'expected'), [
        ([0, 1, 1, 2], None, [0, 1, 2]),
        ('0112', int, ['0', '1', '2']),
        (range(10), lambda x: x % 3, [0, 1, 2]),
        (['a', 'cd', 'cd', 'e', 'fgh'], None, ['a', 'cd', 'e', 'fgh']),
        (['a', 'cd', 'cd', 'e', 'fgh'], len, ['a', 'cd', 'fgh']),
        ([{'a': 1}, {'a': 2}, {'a': 1}], operator.itemgetter('a'), [{'a': 1}, {'a': 2}]),
    ],
)
def test_unique(seq, key, expected):
    assert seq | Unique(key) | Pipe(list) == expected


def test_exec():
    v = 42

    random.seed(42)
    x = [0, 1, 2]
    assert v | Exec(lambda: random.shuffle(x)) == v
    assert x == [1, 0, 2]

    random.seed(42)
    x = [0, 1, 2]
    assert v | Exec(random.shuffle, x) == v
    assert x == [1, 0, 2]

    u = []
    assert v | Exec(lambda: u.append(1)) == v
    assert u == [1]

    assert v | Exec(u.append, 2) == v
    assert u == [1, 2]

    x = [2, 0, 1]
    assert x | Exec(x.sort, reverse=True) == [2, 1, 0]
