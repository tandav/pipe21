from pipe import *


def test_pipe():
    assert range(5) | Pipe(list) == list(range(5))


def test_map():
    assert range(5) | Map(str) | Pipe(list) == list(map(str, range(5)))


def test_filter():
    i = range(5)
    def is_even(x): return x % 2 == 0
    assert i | Filter(is_even) | Pipe(list) == list(filter(is_even, i))


def test_value_by():
    assert range(2) | ValueBy(str) | Pipe(list) == [(0, '0'), (1, '1')]


def test_unit_tuple():
    assert unit_tuple(1) == (1,)
    assert unit_tuple((1,)) == (1,)
    assert unit_tuple((1,2)) == (1,2)


def test_append():
    assert [(0,), (1,)] | Append(lambda x: str(x[0])) | Pipe(list) == [(0, '0'), (1, '1')]
    assert [(0, '0'), (1, '1')] | Append(lambda x: str(x[0] * 10)) | Pipe(list) == [(0, '0', '0'), (1, '1', '10')]
