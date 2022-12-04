from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from pathlib import Path
from typing import Any
from typing import Callable
from typing import TypeVar

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# todo: add f and kw annotations for every class

class B:
    f: Callable[..., Any]
    kw: Any
    def __init__(self, f: Callable[..., Any] | None = None, **kw: Any) -> None: ...

class Pipe(B):
    f: Callable[[T], V]
    def __ror__(self, x: T) -> V: ...

class Map(B):
    f: Callable[[K], V]
    def __ror__(self, x: Iterable[K]) -> Iterator[V]: ...

class Filter(B):
    def __ror__(self, x: Iterable[T]) -> Iterator[T]: ...

class Reduce(B):
    def __ror__(self, x: Iterable[T]) -> Any: ...

class MapValues(B):
    def __ror__(self, it: Iterable[tuple[K, V]]) -> Iterator[tuple[K, T]]: ...

class MapKeys(B):
    def __ror__(self, it: Iterable[tuple[K, V]]) -> Iterator[tuple[T, V]]: ...

class FilterFalse(B):
    def __ror__(self, it: Iterable[Any]) -> Iterator[Any]: ...

class FilterKeys(B):
    def __ror__(self, it: Iterable[tuple[K, V]]) -> Iterator[tuple[K, V]]: ...

class FilterValues(B):
    def __ror__(self, it: Iterable[tuple[K, V]]) -> Iterator[tuple[K, V]]: ...

class FlatMap(B):
    def __ror__(self, x: Iterable[T]) -> Iterator[V]: ...

class FlatMapValues(B):
    def __ror__(self, it: Iterable[tuple[K, V]]) -> Iterator[tuple[K, T]]: ...

class KeyBy(B):
    def __ror__(self, it: Iterable[V]) -> Iterator[tuple[K, V]]: ...

class ValueBy(B):
    def __ror__(self, it: Iterable[K]) -> Iterator[tuple[K, V]]: ...

class Append(B):
    def __ror__(self, it: Iterable[Iterable[Any]]) -> Iterable[Iterable[Any]]: ...

class Keys(B):
    def __ror__(self, it: Iterable[tuple[K, V]]) -> Iterator[K]: ...

class Values(B):
    def __ror__(self, it: Iterable[tuple[K, V]]) -> Iterator[V]: ...

class Grep(B):
    def __ror__(self, x: Iterable[T]) -> Iterator[T]: ...

class GrepV(B):
    def __ror__(self, x: Iterable[T]) -> Iterator[T]: ...

class FilterEqual(B):
    def __ror__(self, x: Iterable[T]) -> Iterator[T]: ...

class FilterNotEqual(B):
    def __ror__(self, x: Iterable[T]) -> Iterator[T]: ...

class Count(B):
    def __ror__(self, x: Iterable[T]) -> int: ...

class Take(B):
    def __ror__(self, x: Iterable[T]) -> tuple[T, ...]: ...

class Chunked(B):
    def __ror__(self, x: Iterable[T]) -> Iterable[tuple[T, ...]]: ...

class GroupBy(B):
    def __ror__(self, x: Iterable[T]) -> Iterator[tuple[T, Iterator[T]]]: ...

class ReadLines(B):
    def __ror__(self, fn: str | Path) -> list[str]: ...

class ShellExec(B):
    def __ror__(self, x: Sequence[str]) -> list[str]: ...

class PipeArgs(B):
    def __ror__(self, x: Iterable[Any]) -> Any: ...

class MapArgs(B):
    def __ror__(self, x: Iterable[Iterable[Any]]) -> Iterable[Any]: ...

class IsUnique(B):
    def __ror__(self, seq: Sequence[Any]) -> bool: ...

class Sorted(B):
    def __ror__(self, x: Iterable[T]) -> list[T]: ...

class Unique(B):
    def __ror__(self, it: Iterable[T]) -> Generator[T, None, None]: ...

class ForEach(B):
    def __ror__(self, x: Any) -> None: ...

class ThreadMap(B):
    def __ror__(self, x: Iterable[T]) -> tuple[V]: ...

class ProcessMap(B):
    def __ror__(self, x: Iterable[T]) -> tuple[V]: ...
