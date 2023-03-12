from pipe21 import *


def types_pipe(x: int) -> str:
    return x | Pipe(str)


def f0(x: str) -> frozenset[int]:
    return frozenset(x | Map(int))


def f1(x: str) -> frozenset[str]:
# def f1(x: str) -> frozenset[int]:
    return (
        x
        | Map(int)
        | Pipe(frozenset)
    )


# def bits_to_intervals(x: str) -> frozenset[int]:
#     return (
#         x
#         | P.Map(int)
#         | P.Pipe(enumerate)
#         | P.FilterValues()
#         | P.Keys()
#         | P.Pipe(frozenset)
#     )
