# Duration arithmetic

In `solution.py`, implement `Duration`, a length of time in whole
seconds that supports natural arithmetic and ordering.

```python
class Duration:
    def __init__(self, seconds: int):
        """Store as `self.seconds` (int)."""
```

Required behaviour (all results are new `Duration` objects unless
stated otherwise):

**Addition**
- `Duration(60) + Duration(30)` → `Duration(90)`
- `Duration(60) + 30` → `Duration(90)` (plain ints are seconds)
- `30 + Duration(60)` → `Duration(90)` — the REFLECTED case: int's own
  `__add__` fails, so Python asks your `__radd__`.
- Because `0 + Duration(x)` works, `sum([d1, d2, d3])` works too — the
  grader checks it.
- `Duration(1) + "x"` → `TypeError` (return `NotImplemented` from the
  dunder; don't raise yourself, or the reflected protocol breaks).

**Multiplication**
- `Duration(60) * 3` and `3 * Duration(60)` → `Duration(180)`
  (`__mul__` + `__rmul__`; int factors only, others → `TypeError`).

**Ordering & equality**
- `==` / `!=` by seconds; comparing with a non-Duration is `False`,
  never an error.
- `<`, `<=`, `>`, `>=` between Durations compare seconds. `sorted()`
  on a list of Durations must work. Comparing order with a non-Duration
  raises `TypeError` (return `NotImplemented`).

Edge cases: `Duration(0)` behaves normally; operations never mutate
their operands.

Examples:

```python
>>> (Duration(90) + Duration(30)).seconds
120
>>> (15 + Duration(45)).seconds
60
>>> sum([Duration(1), Duration(2), Duration(3)]).seconds
6
>>> Duration(59) < Duration(60), Duration(60) >= Duration(60)
(True, True)
>>> sorted([Duration(3), Duration(1), Duration(2)])[0].seconds
1
```
