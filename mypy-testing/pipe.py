class Pipe:
    def __init__(self, f):
        self.f = f

    def __ror__(self, x):
        return self.f(x)

# def bits_to_intervals(bits: int) -> str:
#     return bits | Pipe(str)

# def f(x):
#     return x + 1

# def f(x: int) -> str:
#     return x + 1
