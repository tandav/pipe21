import abc
from collections.abc import Callable
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Protocol
from typing import TypeVar

__version__: str = ...

T = TypeVar('T')
U = TypeVar('U')
_T_co = TypeVar("_T_co", covariant=True)


class PipedIterator(Iterable[_T_co], Protocol[_T_co]):
    def __or__(self, x: Any) -> Any: ...
    @abc.abstractmethod
    def __next__(self) -> _T_co: ...
    def __iter__(self) -> Iterator[_T_co]: ...


class B(Generic[T, U]):
    def __init__(self, f: Callable[[T], U], **kw: Any) -> None:
        ...

class Pipe(B[T, U]):
    def __ror__(self, x: T) -> U: ...


class Map(B[T, U]):
    def __ror__(self, x: Iterable[T]) -> PipedIterator[U]: ...


class Filter(B[T, U]):
    def __ror__(self, x: Iterable[T]) -> PipedIterator[U]: ...
