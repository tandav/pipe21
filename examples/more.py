class Base:
    
    def __init__(self, op):
        self.op = op
    
    def __call__(self, *args, **kw):
        self.args = args
        self.kw = kw
        return self
    
    def __ror__(self, other):
        return self.op(self, other)

# base pack
Pipe   = Base(lambda self, other: self.args[0](other))
Map    = Base(lambda self, other: map(self.args[0], other))
Sorted = Base(lambda self, other: sorted(other[0], reverse=self.args[1]))
# Filter = Base(lambda self, other: filter(self.f, it))
# Reduce = Base(lambda self, other: reduce(self.f, it))


(
    23423546 
    | Pipe(float)
    | Pipe(str)
    | Pipe(len)
    | Pipe(range)
    | Map(lambda x: x * 10)
    | Pipe(list)
    | Sorted()
)




class Base:
    
    def __init__(self, op):
        self.op = op
    
    def __call__(self, f):
        self.f = f
        return self
    
    def __ror__(self, other):
        return self.op(self, other)

# base pack
Pipe   = Base(lambda self, v: self.f(v))
# Map    = Base(lambda self, it: map(self.f, it))
# Filter = Base(lambda self, it: filter(self.f, it))
# Reduce = Base(lambda self, it: reduce(self.f, it))

# extended pack
# Shell = Base()

(
    23423546 
    | Pipe(float) 
#     | Pipe(str)
#     | Pipe(len)
#     | Pipe(range)
#     | Filter(lambda x: x % 2)
#     | Pipe(list)
)
