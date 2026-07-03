# Records without boilerplate

`dataclasses` writes `__init__`, `__eq__`, ordering and more for you. In
`solution.py`, define two dataclasses:

## 1. `Book`

Fields, in this order:

- `title` (str) — required
- `author` (str) — required
- `pages` (int) — defaults to `0`
- `tags` (list of str) — defaults to a **new empty list per instance**

Behaviour:

- Constructible positionally and by keyword: `Book("T", "A")`,
  `Book(title="T", author="A", pages=10, tags=["x"])`.
- Two books with equal field values compare equal; different values don't.
- The `tags` default must not be shared: mutating one fresh book's `tags`
  must not affect another's (a plain `tags=[]` default would — that's the
  `field(default_factory=list)` lesson).

## 2. `Point`

An **immutable, ordered** dataclass with fields `x` then `y` (both numbers):

- Assigning to an attribute of an existing `Point` raises an error
  (frozen dataclasses raise a subclass of `AttributeError`).
- Points are hashable: usable as dict keys / set members, and
  `Point(1, 2) == Point(1, 2)` implies one entry in a set.
- Points support `<`, `<=`, `>`, `>=` comparing field-by-field in
  definition order (x first, then y) — so `sorted()` just works.

Example:

```python
>>> a = Book("Dune", "Herbert")
>>> a.pages, a.tags
(0, [])
>>> a == Book("Dune", "Herbert")
True
>>> sorted([Point(2, 1), Point(1, 9), Point(1, 2)])
[Point(x=1, y=2), Point(x=1, y=9), Point(x=2, y=1)]
>>> len({Point(1, 2), Point(1, 2)})
1
```
