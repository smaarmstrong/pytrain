# PEP 695 generics

Python 3.12 added dedicated syntax for generics: type parameters are declared
in square brackets right on the `def`/`class`, no explicit `TypeVar` needed.
In `solution.py`, use **PEP 695 syntax only** (no `typing.TypeVar`, no
`Generic[...]` base class) to write:

```python
def pick[T](items: Sequence[T], index: int) -> T:
    """items[index] (let IndexError propagate)."""

def swap[A, B](pair: tuple[A, B]) -> tuple[B, A]:
    """(x, y) -> (y, x)."""

class Pair[T]:
    """Pair(first, second): two values of the same type.

    .first / .second   attributes
    .swapped()         a NEW Pair with the elements exchanged
    .as_tuple()        (first, second)
    """
```

The grader checks `pick.__type_params__`, `swap.__type_params__` and
`Pair.__type_params__` — these are only populated by the new syntax, so
old-style TypeVars won't pass.

Examples:

```python
>>> pick(["a", "b", "c"], 1)
'b'
>>> swap((1, "x"))
('x', 1)
>>> p = Pair(1, 2).swapped()
>>> p.as_tuple()
(2, 1)
```
