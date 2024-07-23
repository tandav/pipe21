class B:
    def __init__(self, f=None, *args, **kw):
        self.f = f
        self.args = args
        self.kw = kw


class Pipe  (B): __ror__ = lambda self, x: self.f(x, *self.args, **self.kw)
class Map   (B): __ror__ = lambda self, it: (self.f(x) for x in it)
class Filter(B): __ror__ = lambda self, it: (x for x in it if self.f(x))
