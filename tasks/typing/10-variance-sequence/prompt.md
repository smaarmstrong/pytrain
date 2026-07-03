# Variance and Sequence-friendly APIs

Two habits of well-typed APIs: read-only containers can be **covariant**
(a `Box[Circle]` is usable as a `Box[Shape]`), and functions that only *read*
a sequence should accept `Sequence[...]`, not `list[...]` — so tuples,
ranges and custom sequences all work.

In `solution.py`:

```python
T_co = TypeVar("T_co", covariant=True)

class Box(Generic[T_co]):
    """An immutable read-only wrapper: Box(value).get() -> the value.

    Because Box only produces its value (never consumes one), its type
    parameter is declared covariant. (PEP 695 `class Box[T]:` with inferred
    variance is also accepted.)
    """
    def get(self) -> T_co: ...


def total(nums: Sequence[float]) -> float:
    """Sum of nums. Annotate with Sequence so tuples and ranges are accepted."""

def labels_upper(labels: Sequence[str]) -> list[str]:
    """Each label upper-cased, as a new list, in order."""
```

Requirements:

- `Box`'s type variable is covariant: either a classic
  `TypeVar(..., covariant=True)` or a PEP 695 type parameter (which infers
  variance).
- `total` and `labels_upper` must have their parameter annotated with
  `Sequence[...]` (the grader inspects the hints) and must genuinely work on
  lists, tuples, ranges and grader-defined `collections.abc.Sequence`
  subclasses.
- `total(()) == 0` and `labels_upper([]) == []`.

Examples:

```python
>>> Box("hi").get()
'hi'
>>> total(range(4))
6
>>> labels_upper(("a", "b"))
['A', 'B']
```
