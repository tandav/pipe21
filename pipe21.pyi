from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from typing import Any
from typing import Generic
from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')


class B(Generic[T, U]):
    def __init__(self, f: Callable[[T], U], **kw: Any) -> None:
        ...


class Pipe(B[T, U]):
    def __ror__(self, x: T) -> U: ...


class Map(B[T, U]):
    def __ror__(self, x: Iterable[T]) -> Iterator[U]: ...


class Filter(B[T, U]):
    def __ror__(self, x: Iterable[T]) -> Iterator[U]: ...
