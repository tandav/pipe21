# from typing import Any, Callable, TypeVar

# T = TypeVar('T')
# U = TypeVar('U')

# class Pipe:
#     """
#     A class that represents a pipe that can be used to apply functions to data.
#     """
#     def __init__(self, f: Callable[[T], U]):
#         self.f = f

#     def __ror__(self, x: T) -> U:
#         """
#         Applies the function f to the input x and returns the result.
#         """
#         return self.f(x)


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

def bits_to_intervals(bits: int) -> str:
    return bits | Pipe(str)
