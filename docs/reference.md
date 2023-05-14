# reference

```py
>>> from pipe21 import *

```

## Pipe
Put a value into a function as 1st argument

```py
>>> range(5) | Pipe(list)
[0, 1, 2, 3, 4]

>>> 2 | Pipe(pow, 8)
256

>>> 'FF' | Pipe(int, base=16)
255

>>> b'\x02\x00' | Pipe(int.from_bytes, byteorder='big')
512

>>> 'ab' | Pipe(enumerate, start=0) | Pipe(list)
[(0, 'a'), (1, 'b')]

>>> import math
>>> 5.01 | Pipe(math.isclose, 5, abs_tol=0.01)
True

>>> import random
>>> random.seed(44)
>>> [0, 1, 2] | Pipe(random.choices, [0.8, 0.15, 0.05], k=20)
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0]

>>> import itertools
>>> [0, 1, 2] | Pipe(itertools.zip_longest, 'ab', fillvalue=None) | Pipe(list)
[(0, 'a'), (1, 'b'), (2, None)]

>>> import operator
>>> [0, 1, 2] | Pipe(itertools.accumulate, operator.add, initial=100) | Pipe(list)
[100, 100, 101, 103]

```

## Map

```py
>>> range(5) | Map(str) | Pipe(''.join)
'01234'

```

## Filter

```py
>>> range(5) | Filter(lambda x: x % 2 == 0) | Pipe(list)
[0, 2, 4]

```

## Reduce

```py
>>> import operator
>>> range(5) | Reduce(operator.add)
10

>>> range(5) | Reduce(operator.add, 5)  # with initial value
15

```

## MapKeys

```py
>>> [(1, 10), (2, 20)] | MapKeys(str) | Pipe(list)
[('1', 10), ('2', 20)]

```

## MapValues

```py
>>> [(1, 10), (2, 20)] | MapValues(str) | Pipe(list)
[(1, '10'), (2, '20')]

```

## FilterFalse
Same as `Filter` but negative

```py
>>> range(5) | FilterFalse(lambda x: x % 2 == 0) | Pipe(list)
[1, 3]

```

## FilterKeys

Take `(k, v)` pairs iterable and keep only elements for which `predicate(k) == True`. If no predicate function is provided - default function `bool` will be used.

```py
>>> [(0, 2), (3, 0)] | FilterKeys() | Pipe(list)
[(3, 0)]

>>> [(0, 2), (3, 0)] | FilterKeys(lambda x: x % 2 == 0) | Pipe(list)
[(0, 2)]

```

## FilterValues

Same as `FilterKeys` but for `v` in `(k, v)` pairs

```py
>>> [(0, 2), (3, 0)] | FilterValues() | Pipe(list)
[(0, 2)]

>>> [(0, 2), (3, 0)] | FilterValues(lambda x: x % 2 == 0) | Pipe(list)
[(0, 2), (3, 0)]

```

## FlatMap

```py
>>> [0, 2, 3, 0, 4] | FlatMap(range) | Pipe(list)
[0, 1, 0, 1, 2, 0, 1, 2, 3]

>>> [2, 3, 4] | FlatMap(lambda x: [(x, x), (x, x)]) | Pipe(list)
[(2, 2), (2, 2), (3, 3), (3, 3), (4, 4), (4, 4)]

>>> def yield_even(it):
...     for x in it:
...         if x % 2 == 0:
...             yield x
>>> [range(0, 5), range(100, 105)] | FlatMap(yield_even) | Pipe(list)
[0, 2, 4, 100, 102, 104]

```

## FlatMapValues

```py
>>> [("a", ["x", "y", "z"]), ("b", ["p", "r"])] | FlatMapValues(lambda x: x) | Pipe(list)
[('a', 'x'), ('a', 'y'), ('a', 'z'), ('b', 'p'), ('b', 'r')]

>>> keep_even = lambda it: it | Filter(lambda x: x % 2 == 0)
>>> [('a', [0, 1, 2]), ('b', [3, 4])] | FlatMapValues(keep_even) | Pipe(list)
[('a', 0), ('a', 2), ('b', 4)]

```

## KeyBy

```py
>>> range(2) | KeyBy(str) | Pipe(list)
[('0', 0), ('1', 1)]

```

## ValueBy

```py
>>> range(2) | ValueBy(str) | Pipe(list)
[(0, '0'), (1, '1')]

```

## Append

```py
>>> [(0,), (1,)] | Append(lambda x: str(x[0])) | Pipe(list)
[(0, '0'), (1, '1')]

>>> [(0, '0'), (1, '1')] | Append(lambda x: str(x[0] * 10)) | Pipe(list)
[(0, '0', '0'), (1, '1', '10')]

```

## Keys

```py
>>> [(0, 'a'), (1, 'b')] | Keys() | Pipe(list)
[0, 1]

```

## Values

```py
>>> [(0, 'a'), (1, 'b')] | Values() | Pipe(list)
['a', 'b']

```

## Grep

```py
>>> ['hello 42 bro', 'world', 'awesome 42'] | Grep('42') | Pipe(list)
['hello 42 bro', 'awesome 42']

# regex is supported (passed to re.search)
>>> ['foo1', 'foo2', '3foo', 'bar1'] | Grep('^foo.*') | Pipe(list)
['foo1', 'foo2']

```

## GrepV

```py
>>> ['hello 42 bro', 'world', 'awesome 42'] | GrepV('42') | Pipe(list)
['world']
>>> ['foo1', 'foo2', '3foo', 'bar1'] | GrepV('^foo.*') | Pipe(list)
['3foo', 'bar1']

```

## Count

useful for objects that don't have `__len__` method:

```py
>>> iter(range(3)) | Count()
3

```

## Slice

```py
>>> range(5) | Slice(2) | Pipe(list)
[0, 1]
>>> range(5) | Slice(2, 4) | Pipe(list)
[2, 3]
>>> range(5) | Slice(2, None) | Pipe(list)
[2, 3, 4]
>>> range(5) | Slice(0, None, 2) | Pipe(list)
[0, 2, 4]

```

## Take

```py
>>> range(5) | Take(3)
(0, 1, 2)

```

## Chunked

```py
>>> range(5) | Chunked(2) | Pipe(list)
[(0, 1), (2, 3), (4,)]

>>> range(5) | Chunked(3) | Pipe(list)
[(0, 1, 2), (3, 4)]

```

## Sorted

```py
>>> '3510' | Sorted()
['0', '1', '3', '5']

>>> '3510' | Sorted(reverse=True)
['5', '3', '1', '0']

>>> '!*&)#' | Sorted(key=ord)
['!', '#', '&', ')', '*']

>>> '!*&)#' | Sorted(key=ord, reverse=True)
['*', ')', '&', '#', '!']

```

## GroupBy

Note: `GroupBy` sorts iterable before grouping. If you pass key function, eg `GroupBy(len)`, it also will be used as sorting key.

```py
>>> import operator
>>> [(0, 'a'), (1, 'c'), (0, 'b'), (2, 'd')] | GroupBy(operator.itemgetter(0)) | MapValues(list) | Pipe(list)
[(0, [(0, 'a'), (0, 'b')]), (1, [(1, 'c')]), (2, [(2, 'd')])]

>>> ['ab', 'cd', 'e', 'f', 'gh', 'ij'] | GroupBy(len) | MapValues(list) | Pipe(list)
[(1, ['e', 'f']), (2, ['ab', 'cd', 'gh', 'ij'])]

```

## IsUnique

```py
>>> [0, 1, 2, 3] | IsUnique()
True
>>> [0, 1, 1, 3] | IsUnique()
False
>>> '0123' | IsUnique(int)
True
>>> '0113' | IsUnique(int)
False

```

## ReduceByKey

```py
>>> import operator
>>> [('a', 1), ('b', 1), ('a', 1)] | ReduceByKey(operator.add)
[('a', 2), ('b', 1)]

```

## PipeArgs

```py
>>> (1, 2) | PipeArgs(operator.add)
3

>>> ('FF', 16) | PipeArgs(int)
255

>>> ([1, 2], 'A') | PipeArgs(dict.fromkeys)
{1: 'A', 2: 'A'}

>>> ({1, 2}, {3, 4, 5}) | PipeArgs(set.union)
{1, 2, 3, 4, 5}

```

## StarMap

```py
>>> [(2, 5), (3, 2), (10, 3)] | StarMap(pow) | Pipe(list)
[32, 9, 1000]
>>> [('00', 16), ('A5', 16), ('FF', 16)] | StarMap(int) | Pipe(list)
[0, 165, 255]

```

## MapApply

```py
>>> import random
>>> random.seed(42)
>>> range(3, 5) | Map(range) | Map(list) | MapApply(random.shuffle) | Pipe(list)
[[1, 0, 2], [3, 1, 2, 0]]

>>> def setitem(key, value):
...     def inner(x):
...         x[key] = value
...     return inner
>>> [{'hello': 'world'}] | MapApply(setitem('foo', 'bar')) | Pipe(list)
[{'hello': 'world', 'foo': 'bar'}]

```

## Unique

```py
>>> ['a', 'cd', 'cd', 'e', 'fgh'] | Unique() | Pipe(list)
['a', 'cd', 'e', 'fgh']

>>> ['a', 'cd', 'cd', 'e', 'fgh'] | Unique(len) | Pipe(list)
['a', 'cd', 'fgh']

```

## Apply

```py
>>> import random
>>> random.seed(42)
>>> range(5) | Pipe(list) | Apply(random.shuffle)
[3, 1, 2, 4, 0]

```

## IterLines

```py
>>> import tempfile
>>> f = tempfile.NamedTemporaryFile('w+')
>>> f.write('hello\nworld\n')
12
>>> f.seek(0)
0
>>> f.name | IterLines() | Pipe(list)
['hello\n', 'world\n']

```
