# Shelf: a custom container

In `solution.py`, implement `Shelf` — a read-only container of book
titles that plays nicely with `len()`, indexing, slicing, `in`, and
`for` loops.

```python
class Shelf:
    def __init__(self, titles):
        """`titles` is any iterable of strings. Store a COPY: mutating
        the original iterable/list afterwards must not affect the Shelf."""
```

Required behaviour:

- `len(shelf)` — number of titles.
- `shelf[0]`, `shelf[-1]` — integer indexing incl. negative indices;
  out-of-range raises `IndexError` (the natural list behaviour).
- `shelf[1:3]` — slicing returns a **new `Shelf`** (not a list) holding
  the sliced titles. All standard slice semantics (steps, open ends).
- `"Dune" in shelf` — exact title membership (case-sensitive).
- `for t in shelf:` / `list(shelf)` — iterates titles in order. The
  Shelf must be re-iterable: iterating twice yields the full sequence
  both times, and two simultaneous iterators don't interfere.
- Empty shelf: `len == 0`, `list(...) == []`, any `in` is False, and it
  is falsy in a boolean context (`bool(Shelf([])) is False`) — you get
  this for free from `__len__`.

Examples:

```python
>>> s = Shelf(["Dune", "Emma", "Hamlet"])
>>> len(s)
3
>>> s[-1]
'Hamlet'
>>> sub = s[0:2]
>>> isinstance(sub, Shelf), list(sub)
(True, ['Dune', 'Emma'])
>>> "Emma" in s, "emma" in s
(True, False)
>>> [t for t in s]
['Dune', 'Emma', 'Hamlet']
```
