import pipe21 as P


def f0(x: str) -> frozenset[int]:
    return frozenset(x | P.Map(int))


def f1(bits: str) -> frozenset[int]:
    q = bits | P.Map(int)
    reveal_type(q)
    v = P.Pipe(frozenset)
    reveal_type(v)
    u = q | v
    reveal_type(u)
    return u

    # return (
    #     bits
    #     | P.Map(int)
    #     | P.Pipe(frozenset)
    # )


# def bits_to_intervals(bits: str) -> frozenset[int]:
#     return (
#         bits
#         | P.Map(int)
#         | P.Pipe(enumerate)
#         | P.FilterValues()
#         | P.Keys()
#         | P.Pipe(frozenset)
#     )
