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

>>> [{1, 2}, {2, 3, 4}, {4, 5}] | Reduce(operator.or_)
{1, 2, 3, 4, 5}

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

>>> [range(0, 5), range(100, 105)] | FlatMap(lambda it: (x for x in it if x % 2 == 0)) | Pipe(list)
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
>>> ['hello foo', 'world', 'awesome FOo'] | Grep('foo') | Pipe(list)
['hello foo']

# regex is supported (passed to re.search)
>>> ['foo1', 'foo2', '3foo', 'bar1'] | Grep('^foo.*') | Pipe(list)
['foo1', 'foo2']

# case-insensitive
>>> ['hello foo', 'world', 'awesome FOo'] | Grep('foo', i=True) | Pipe(list)
['hello foo', 'awesome foo']
>>> ['hello foo', 'world', 'awesome FOo'] | Grep('Foo', i=True) | Pipe(list)
['hello foo', 'awesome foo']

```

## GrepV

```py
>>> ['hello foo', 'world', 'awesome FOo'] | GrepV('foo') | Pipe(list)
['world', 'awesome FOo']
>>> ['foo1', 'foo2', '3foo', 'bar1'] | GrepV('^foo.*') | Pipe(list)
['3foo', 'bar1']

# case-insensitive
>>> ['hello foo', 'world', 'awesome FOo'] | GrepV('foo', i=True) | Pipe(list)
['world']
>>> ['hello foo', 'world', 'awesome FOo'] | GrepV('Foo', i=True) | Pipe(list)
['world']

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
['hello', 'world']

>>> f.name | IterLines(strip=False) | Pipe(list)
['hello\n', 'world\n']

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

## ReduceByKey

```py
>>> import operator
>>> [('a', 1), ('b', 1), ('a', 1)] | ReduceByKey(operator.add)
[('a', 2), ('b', 1)]

```

## Apply

```py
>>> import random
>>> random.seed(42)
>>> range(5) | Pipe(list) | Apply(random.shuffle)
[3, 1, 2, 4, 0]

```

## StarPipe

```py
>>> (1, 2) | StarPipe(operator.add)
3

>>> ('FF', 16) | StarPipe(int)
255

>>> ([1, 2], 'A') | StarPipe(dict.fromkeys)
{1: 'A', 2: 'A'}

>>> ({1, 2}, {3, 4, 5}) | StarPipe(set.union)
{1, 2, 3, 4, 5}

```

## StarMap

```py
>>> [(2, 5), (3, 2), (10, 3)] | StarMap(pow) | Pipe(list)
[32, 9, 1000]
>>> [('00', 16), ('A5', 16), ('FF', 16)] | StarMap(int) | Pipe(list)
[0, 165, 255]

```

## StarFlatMap

```py
>>> range(2, 10) | Pipe(itertools.permutations, r=2) | StarFlatMap(lambda a, b: [(a, b)] if a % b == 0 else []) | Pipe(list)
[(4, 2), (6, 2), (6, 3), (8, 2), (8, 4), (9, 3)]

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

## Switch

```py
>>> cases = [
...     (lambda i: i % 3 == i % 5 == 0, lambda x: 'FizzBuzz'),
...     (lambda i: i % 3 == 0, lambda x: 'Fizz'),
...     (lambda i: i % 5 == 0, lambda x: 'Buzz'),
...     (lambda i: i > 100, lambda x: f'{x} is large'),
... ]
>>> 1 | Switch(cases)
1
>>> 3 | Switch(cases)
'Fizz'
>>> 5 | Switch(cases)
'Buzz'
>>> 15 | Switch(cases)
'FizzBuzz'
>>> 101 | Switch(cases)
'101 is large'

```

## MapSwitch

```py
>>> range(1, 20) | MapSwitch(cases) | Pipe(list)
[1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16, 17, 'Fizz', 19]
>>> range(5) | MapSwitch([(lambda x: x % 2 == 0, lambda x: x * 100)]) | Pipe(list)
[0, 1, 200, 3, 400]

```

## YieldIf
Takes a function to map values (optional, by default there's no mapping) and a key. If key is false, value will not be yielded. Key is optional, default is `bool`

```py
>>> range(5) | YieldIf(lambda x: x * 100) | Pipe(list)
[100, 200, 300, 400]
>>> range(5) | YieldIf(lambda x: x * 100, key=lambda x: x % 2 == 0) | Pipe(list)
[0, 200, 400]
>>> range(5) | YieldIf(key=lambda x: x % 2 == 0) | Pipe(list)
[0, 2, 4]
>>> range(5) | YieldIf() | Pipe(list)
[1, 2, 3, 4]

```

## Join
```py
>>> range(5) | Join(range(2, 5)) | Pipe(list)
[(2, 2), (3, 3), (4, 4)]

>>> range(1, 7) | Join(range(2, 6), key=lambda x, y: x % y == 0) | Pipe(list)
[(2, 2), (3, 3), (4, 2), (4, 4), (5, 5), (6, 2), (6, 3)]

```

## GetItem

```py
>>> {'a': 'b'} | GetItem('a')
'b'

```

## SetItem

```py
>>> {'a': 'b'} | SetItem('foo', 'bar')
{'a': 'b', 'foo': 'bar'}

```

## DelItem

```py
>>> {'a': 'b'} | DelItem('a')
{}

```

## GetAttr

```py
>>> from types import SimpleNamespace
>>> SimpleNamespace(a='b') | GetAttr('a')
'b'

```

## SetAttr

```py
>>> SimpleNamespace(a='b') | SetAttr('foo', 'bar')
namespace(a='b', foo='bar')

```

## DelAttr

```py
>>> SimpleNamespace(a='b') | DelAttr('a')
namespace()

```

## MapGetItem

```py
>>> [{'a': 'b'}] | MapGetItem('a') | Pipe(list)
['b']

```

## MapSetItem

```py
>>> [{'a': 'b'}] | MapSetItem('foo', 'bar') | Pipe(list)
[{'a': 'b', 'foo': 'bar'}]

```

## MapDelItem

```py
>>> [{'a': 'b'}] | MapDelItem('a') | Pipe(list)
[{}]

```

## MapGetAttr

```py
>>> [SimpleNamespace(a='b')] | MapGetAttr('a') | Pipe(list)
['b']

```

## MapSetAttr

```py
>>> [SimpleNamespace(a='b')] | MapSetAttr('foo', 'bar') | Pipe(list)
[namespace(a='b', foo='bar')]

```

## MapDelAttr

```py
>>> [SimpleNamespace(a='b')] | MapDelAttr('a') | Pipe(list)
[namespace()]

```

## MethodCaller

```py
>>> class K:
...     def hello(self):
...         return 'hello'
...     def increment(self, i, add=1):
...         return i + add
>>> k = K()
>>> k | MethodCaller('hello')
'hello'
>>> k | MethodCaller('increment', 1)
2
>>> k | MethodCaller('increment', 1, add=2)
3

```

## MapMethodCaller

```py
>>> [k] | MapMethodCaller('hello') | Pipe(list)
['hello']

```

## Unique

```py
>>> ['a', 'cd', 'cd', 'e', 'fgh'] | Unique() | Pipe(list)
['a', 'cd', 'e', 'fgh']

>>> ['a', 'cd', 'cd', 'e', 'fgh'] | Unique(len) | Pipe(list)
['a', 'cd', 'fgh']

>>> [{'a': 1}, {'a': 2}, {'a': 1}] | Unique(operator.itemgetter('a')) | Pipe(list)
[{'a': 1}, {'a': 2}]

```

## Exec

```py
>>> v = 42
>>> random.seed(42)
>>> x = [0, 1, 2]

>>> v | Exec(lambda: random.shuffle(x))
42
>>> x
[1, 0, 2]

>>> random.seed(42)
>>> x = [0, 1, 2]
>>> v | Exec(random.shuffle, x)
42
>>> x
[1, 0, 2]
>>> u = []
>>> v | Exec(lambda: u.append(1))
42
>>> u
[1]
>>> v | Exec(u.append, 2)
42
>>> u
[1, 2]
>>> x = [2, 0, 1]
>>> x | Exec(x.sort, reverse=True)
[2, 1, 0]

```
