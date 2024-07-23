# mypy minimal example


Type annotations are in a separate stub file [`pipe21.pyi`](pipe21.pyi) to keep the methods as one-liners in the `pipe21.py` file.

The file `mypy_test.py` contains a few functions to test if the type annotations are correct and working. The last function does not have correct types according to mypy:

```shell
$ mypy mypy_test.py 
mypy_test.py:18: error: Unsupported operand types for | ("Iterator[int]" and "Pipe[Iterable[_T_co], FrozenSet[_T_co]]")
mypy_test.py:18: error: Incompatible return value type (got "FrozenSet[_T_co]", expected "FrozenSet[int]")
Found 2 errors in 1 file (checked 1 source file)
```
