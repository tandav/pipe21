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

## `MapValues`   

## `MapKeys`     

## `FilterKeys`  

## `FilterValues`

## `FlatMap`

## `KeyBy`         

## `ValueBy`       

## `Append`        

## `Keys`          

## `Values`        

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

## `ReadLines`     

## `ShellArg`

## `ShellExec`     

## `PipeArgs`      

## `MapArgs`       

## `ForEach`

## `ThreadMap`

## `ProcessMap`

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
