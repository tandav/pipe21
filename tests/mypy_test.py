import pipe21 as P

# def bits_to_intervals(bits: str) -> frozenset[int]:
#     return (
#         bits
#         | P.Map(int)
#         | P.Pipe(enumerate)
#         | P.FilterValues()
#         | P.Keys()
#         | P.Pipe(frozenset)
#     )


def bits_to_intervals(bits: str) -> frozenset[int]:
    return (
        bits
        | P.Map(int)
        | P.Pipe(frozenset)
    )
