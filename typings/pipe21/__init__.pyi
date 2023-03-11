from collections.abc import Callable
from typing import Generic
from typing import TypeVar

__version__: str = ...

T = TypeVar('T')
U = TypeVar('U')

class B(Generic[T, U]):
    def __init__(self, f: Callable[[T], U]) -> None:
        ...
        # self.f = f

class Pipe(B[T, U]):
    def __ror__(self, x: T) -> U: ...


def f(x: int) -> int: ...
# def f(x) -> int: ...
