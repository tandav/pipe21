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
