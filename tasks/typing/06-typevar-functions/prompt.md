# Generic functions with TypeVar

In `solution.py`, implement three *generic* functions. Their types must flow:
calling `first` on a `list[int]` must be known to mypy to return `int`, not
`Any` and not `object`. Use `typing.TypeVar` (classic style); PEP 695 syntax
is also accepted if your interpreter has it.

```python
def first(items: Sequence[T]) -> T:
    """The first element. Raise ValueError on an empty sequence.
    Must accept any Sequence: lists, tuples, strings, ..."""

def pairs(a: Iterable[T], b: Iterable[U]) -> list[tuple[T, U]]:
    """Zip a and b (stop at the shorter), as a list of tuples."""

def dedupe(items: Iterable[T]) -> list[T]:
    """Unique items, first occurrence wins, order preserved.
    Items are hashable. Must accept any iterable, including generators."""
```

Examples:

```python
>>> first((10, 20))
10
>>> pairs([1, 2, 3], ["x", "y"])
[(1, 'x'), (2, 'y')]
>>> dedupe("abcabc")
['a', 'b', 'c']
```

Grading: behaviour as above, mypy clean on your module with
`--disallow-untyped-defs`, and a grader-written snippet using
`typing.assert_type` to confirm the generics really propagate, e.g.
`assert_type(first([1, 2, 3]), int)` and
`assert_type(pairs([1], ["x"]), list[tuple[int, str]])` must type-check.
