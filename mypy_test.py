from collections.abc import Iterable
from pipe21 import *


def types_pipe(x: int) -> str:
    return x | Pipe(str)


def types_map(x: str) -> Iterable[int]:
    return x | Map(int)


def types_map_in_frozenset(x: str) -> frozenset[int]:
    return frozenset(x | Map(int))


def types_map_pipe_frozenset(x: str) -> frozenset[int]:
    return x | Map(int) | Pipe(frozenset)
