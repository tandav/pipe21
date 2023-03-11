from collections.abc import Callable
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import TypeVar

__version__: str = ...

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
