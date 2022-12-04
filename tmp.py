import pipe21 as P

# 4234 | P.Pipe(int)


# x: tuple[str] = range(3) | P.Map(str) | P.Pipe(tuple)
# q = range(3) | P.Map(str) | P.Pipe(tuple)
q = range(3) | P.Map(str)
# q = map(str, range(3))
reveal_type(q)
# x: tuple[bytes] = range(3) | P.Map(str) | P.Pipe(tuple)
