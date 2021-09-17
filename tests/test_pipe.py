import hypothesis.strategies as st
from hypothesis import given
from pipe21 import *


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_pipe(it):
    assert it | Pipe(list) == list(it)


@given(st.lists(st.integers() | st.characters() | st.floats() | st.booleans() | st.binary()))
def test_map(it):
    assert it | Map(str) | Pipe(list) == list(map(str, it))


@given(st.lists(st.integers()))
def test_filter(it):
    def is_even(x): return x % 2 == 0
    assert it | Filter(is_even) | Pipe(list) == list(filter(is_even, it))


def test_value_by():
    assert range(2) | ValueBy(str) | Pipe(list) == [(0, '0'), (1, '1')]


def test_unit_tuple():
    assert unit_tuple(1) == (1,)
    assert unit_tuple((1,)) == (1,)
    assert unit_tuple((1,2)) == (1,2)


def test_append():
    assert [(0,), (1,)] | Append(lambda x: str(x[0])) | Pipe(list) == [(0, '0'), (1, '1')]
    assert [(0, '0'), (1, '1')] | Append(lambda x: str(x[0] * 10)) | Pipe(list) == [(0, '0', '0'), (1, '1', '10')]