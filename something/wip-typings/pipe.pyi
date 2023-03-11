from collections.abc import Callable
from typing import Generic
from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')

class Pipe(Generic[T, U]):
    def __init__(self, f: Callable[[T], U]) -> None:
        self.f = f

    def __ror__(self, x: T) -> U:
        return self.f(x)

# def bits_to_intervals(bits: int) -> str:
#     return bits | Pipe(str)
