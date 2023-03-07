# all available methods

## `Pipe`
Put a value into a function with 1 argument.

Examples:
```py
>>> range(5) | Pipe(list)
[0, 1, 2, 3, 4]
```

## `Map`

```py
>>> range(5) | Map(str) | Pipe(''.join)
'01234'
```

## `Filter`

```py
>>> range(5) | Filter(lambda x: x % 2 == 0) | Pipe(list)
[0, 2, 4]
```

## `Reduce`

```py
>>> range(5) | Reduce(lambda a, b: a + b)
10
```

## `MapKeys`

```py
>>> [(1, 10), (2, 20)] | MapKeys(str) | Pipe(list)
[('1', 10), ('2', 20)]
```
## `MapValues`

```py
>>> [(1, 10), (2, 20)] | MapValues(str) | Pipe(list)
[(1, '10'), (2, '20')]
```

## `FilterKeys`

## `FilterValues`

## `FlatMap`

```py
>>> [0, 2, 3, 0, 4] | FlatMap(range) | Pipe(list)
[0, 1, 0, 1, 2, 0, 1, 2, 3]

>>> [2, 3, 4] | FlatMap(lambda x: [(x, x), (x, x)]) | Pipe(list)
[(2, 2), (2, 2), (3, 3), (3, 3), (4, 4), (4, 4)]
```
## `FlatMapValues`

```py
>>> [("a", ["x", "y", "z"]), ("b", ["p", "r"])] | FlatMapValues(lambda x: x) | Pipe(list)
[('a', 'x'), ('a', 'y'), ('a', 'z'), ('b', 'p'), ('b', 'r')]
```

## `KeyBy`

```py
>>> range(2) | KeyBy(str) | Pipe(list)
[('0', 0), ('1', 1)]
```

## `ValueBy`

```py
>>> range(2) | ValueBy(str) | Pipe(list)
[(0, '0'), (1, '1')]
```

## `Append`

## `Keys`

```py
>>> [(0, 'a'), (1, 'b')] | Keys() | Pipe(list)
[0, 1]
```

## `Values`

```py
>>> [(0, 'a'), (1, 'b')] | Values() | Pipe(list)
['a', 'b']
```

## `Grep`

## `GrepV`

## `FilterEqual`

## `FilterNotEqual`

## `Count`

```py
>>> 'abc' | Count()
3
```

## `Take`

```py
>>> range(5) | Take(3)
(0, 1, 2)
```

## `Chunked`

```py
>>> range(5) | Chunked(2) | Pipe(list)
[(0, 1), (2, 3), (4,)]

>>> range(5) | Chunked(3) | Pipe(list)
[(0, 1, 2), (3, 4)]
```

## `GroupBy`

```py
>>> [(0, 'a'), (0, 'b'), (1, 'c'), (2, 'd')] | GroupBy(operator.itemgetter(0)) | MapValues(list) | Pipe(list)
[(0, [(0, 'a'), (0, 'b')]), (1, [(1, 'c')]), (2, [(2, 'd')])]

>>> ['ab', 'cd', 'e', 'f', 'gh', 'ij'] | GroupBy(len) | MapValues(list) | Pipe(list)
[(2, ['ab', 'cd']), (1, ['e', 'f']), (2, ['gh', 'ij'])]
```

## `ReadLines`

```bash
cat file.txt
hello
world
```

```py
>>> 'file.txt' | ReadLines()
['hello', 'world']
```

## `ShellArg`

## `ShellExec`

## `PipeArgs`

```py
>>> (1, 2) | PipeArgs(operator.add)
3

>>> ('FF', 16) | PipeArgs(int)
255

>>> ([1, 2], 'A') | PipeArgs(dict.fromkeys)
{1: 'A', 2: 'A'}

>>> ({1, 2}, {3, 4, 5}) | P.PipeArgs(set.union)
{1, 2, 3, 4, 5}
```

## `MapArgs`

## `Sorted`

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

## `Unique`

```py
>>> ['a', 'cd', 'cd', 'e', 'fgh'] | Unique() | Pipe(list)
['a', 'cd', 'e', 'fgh']

>>> ['a', 'cd', 'cd', 'e', 'fgh'] | Unique(len) | Pipe(list)
['a', 'cd', 'fgh']
```

## `Apply`

```py
>>> import random
>>> random.seed(42)
>>> range(5) | Pipe(list) | Apply(random.shuffle)
[3, 1, 2, 4, 0]
```
