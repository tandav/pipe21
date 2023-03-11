from __future__ import annotations
from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from pathlib import Path
from typing import Any
from typing import Callable
from typing import TypeVar
from typing import Generic

from typing import Any, Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')

def pipe(x: T, f: Callable[[T], U]) -> U:
    """
    Applies a function f to the input x and returns the result.
    """
    return f(x)


def double(x: int) -> int:
    return x * 2

x = 5
result = pipe(x, double)
print(result)  # Output: 10


# T = TypeVar('T')
# K = TypeVar('K')
# V = TypeVar('V')
# R = TypeVar('R')

# # todo: add f and kw annotations for every class

# # class B:
# #     f: Callable[..., R]
# #     kw: Any
# #     def __init__(self, f: Callable[..., Any] | None = None, **kw: Any) -> None: ...


# # C = TypeVar('C', bound=Callable[..., Any])
# # C = Callable[[T], R]

# # class Pipe(B):
# class Pipe:
# # class Pipe(Generic[R]):
#     f: Callable[[object], R]
#     # f: C
#     def __ror__(self, x: object) -> R: ...
#     # def __ror__(self, x: T) -> Any: ...
#     # def __ror__(self, x: R) -> R: ...


# # def pipe(x: object, *fs: Callable[[object], R]) -> R: ...


# # class Pipe:
# #     def __init__(self, f: Callable[..., Any] | None = None, **kw: Any) -> None: ...
# #     def hz(self, x: str) -> int: ...
# #     def __ror__(self, x: str) -> int: ...


# # class MyNumber:
# #     def __init__(self, value: int) -> None:
# #         self.value = value
    
# #     def __ror__(self, other: int) -> int:
# #         return self.value | other

# def bits_to_intervals(bits: int) -> str:
#     return bits | Pipe(str)
#     # return pipe(bits, str)
