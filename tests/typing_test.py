"""Checks that types inferred from pipe21.pyi are correct. Verified by mypy, not at runtime."""
import operator
import random
from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from typing import assert_type

from pipe21 import *


def add(a: int, b: int) -> int:
    return a + b


def divisors(a: int, b: int) -> list[tuple[int, int]]:
    return [(a, b)] if a % b == 0 else []


def test_pipe() -> None:
    assert_type(range(5) | Pipe(list), list[int])
    assert_type(range(5) | Pipe(tuple), tuple[int, ...])
    assert_type(range(5) | Pipe(set), set[int])
    assert_type(range(5) | Pipe(frozenset), frozenset[int])
    assert_type([(1, 'a')] | Pipe(dict), dict[int, str])
    assert_type(range(5) | Pipe(sum), int)
    assert_type(range(5) | Map(str) | Pipe(''.join), str)
    assert_type(2 | Pipe(pow, 8), int)
    assert_type('FF' | Pipe(int, base=16), int)
    assert_type(b'\x02\x00' | Pipe(int.from_bytes, byteorder='big'), int)


def test_map_filter() -> None:
    assert_type(range(5) | Map(str), Iterator[str])
    assert_type(range(5) | Filter(lambda x: x % 2 == 0), Iterator[int])
    assert_type(range(5) | FilterFalse(lambda x: x % 2 == 0), Iterator[int])
    assert_type(range(5) | Reduce(add), int)
    assert_type(range(5) | Reduce(operator.add, 100), int)
    assert_type([0, 2] | FlatMap(range), Iterator[int])
    assert_type(range(5) | Unique(), Iterator[int])
    assert_type(range(5) | MapApply(print), Iterator[int])
    assert_type(range(5) | Count(), int)


def test_key_value() -> None:
    assert_type([(1, 10)] | MapKeys(str), Iterator[tuple[str, int]])
    assert_type([(1, 10)] | MapValues(str), Iterator[tuple[int, str]])
    assert_type([(1, 10)] | FilterKeys(), Iterator[tuple[int, int]])
    assert_type([(1, 10)] | FilterValues(lambda x: x > 0), Iterator[tuple[int, int]])
    assert_type([('a', 2)] | FlatMapValues(range), Iterator[tuple[str, int]])
    assert_type(range(2) | KeyBy(str), Iterator[tuple[str, int]])
    assert_type(range(2) | ValueBy(str), Iterator[tuple[int, str]])
    assert_type([(0,), (1,)] | Append(lambda x: str(x[0])), Iterator[tuple[int, str]])
    assert_type([(0, 'a')] | Keys(), Iterator[int])
    assert_type([(0, 'a')] | Values(), Iterator[str])
    assert_type([(0, 'a')] | SwapKV(), Iterator[tuple[str, int]])
    assert_type(['ab', 'c'] | GroupBy(len), Iterator[tuple[int, Iterator[str]]])
    assert_type([('a', 1)] | ReduceByKey(operator.add), list[tuple[str, int]])
    assert_type(range(5) | Join(['a', 'b']), Iterator[tuple[int, str]])


def test_text() -> None:
    assert_type(['hello foo'] | Grep('foo'), Iterator[str])
    assert_type([b'hello foo'] | Grep(b'foo', v=True, i=True), Iterator[bytes])


def test_iter_lines(tmp_path: Path) -> None:
    file = tmp_path / 'file.txt'
    file.write_text('hello\n')
    assert_type(file | IterLines(strip=False), Iterator[str])
    assert_type(str(file) | IterLines(), Iterator[str])


def test_slicing_sorting() -> None:
    assert_type(range(5) | Slice(2), Iterator[int])
    assert_type(range(5) | Slice(0, None, 2), Iterator[int])
    assert_type(range(5) | Take(3), list[int])
    assert_type('3510' | Sorted(key=int, reverse=True), list[str])
    assert_type(range(5) | Chunked(2), Iterator[tuple[int, ...]])


def test_star() -> None:
    assert_type((2, 5) | StarPipe(add), int)
    assert_type([(2, 5)] | StarMap(add), Iterator[int])
    assert_type([(2, 5)] | StarFlatMap(divisors), Iterator[tuple[int, int]])


def test_switch() -> None:
    cases = [(lambda x: x % 2 == 0, lambda x: f'{x} is even')]
    assert_type(1 | Switch(cases), int | str)
    assert_type(range(5) | MapSwitch(cases), Iterator[int | str])
    assert_type(range(5) | YieldIf(), Iterator[int])
    assert_type(range(5) | YieldIf(key=lambda x: x % 2 == 0), Iterator[int])
    assert_type(range(5) | YieldIf(str), Iterator[str])


def test_items_attrs() -> None:
    assert_type({'a': 'b'} | GetItem('a'), str)
    assert_type([1, 2, 3] | GetItem(0), int)
    assert_type({'a': 'b'} | SetItem('foo', 'bar'), dict[str, str])
    assert_type({'a': 'b'} | DelItem('a'), dict[str, str])
    assert_type(SimpleNamespace(a='b') | GetAttr('a'), Any)
    assert_type(SimpleNamespace(a='b') | SetAttr('foo', 'bar'), SimpleNamespace)
    assert_type(SimpleNamespace(a='b') | DelAttr('a'), SimpleNamespace)
    assert_type([{'a': 'b'}] | MapGetItem('a'), Iterator[str])
    assert_type([{'a': 'b'}] | MapSetItem('foo', 'bar'), Iterator[dict[str, str]])
    assert_type([{'a': 'b'}] | MapDelItem('a'), Iterator[dict[str, str]])
    assert_type([SimpleNamespace(a='b')] | MapGetAttr('a'), Iterator[Any])
    assert_type([SimpleNamespace(a='b')] | MapSetAttr('foo', 'bar'), Iterator[SimpleNamespace])
    assert_type([SimpleNamespace(a='b')] | MapDelAttr('a'), Iterator[SimpleNamespace])
    assert_type('ab' | MethodCaller('center', 4, '-'), Any)
    assert_type(['ab'] | MapMethodCaller('upper'), Iterator[Any])


def test_side_effects() -> None:
    assert_type([2, 0, 1] | Apply(random.shuffle), list[int])
    assert_type(42 | Exec(list), int)
