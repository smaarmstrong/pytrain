# Counters and captured loops

Three closure factories in `solution.py`.

```python
def make_counter():
    """Return a zero-argument function. Each call returns 1, 2, 3, ...

    The count lives in the enclosing scope — rebinding it from the
    inner function needs `nonlocal`. Counters from separate
    make_counter() calls are fully independent."""

def make_accumulator(start=0):
    """Return a one-argument function. Each call adds its argument to
    a running total (starting at `start`) and returns the new total.

    acc = make_accumulator(100)
    acc(1)  # 101
    acc(2)  # 103
    """

def make_multipliers(factors):
    """Return a LIST of one-argument functions, one per factor, where
    the i-th function multiplies its argument by factors[i].

    fs = make_multipliers([2, 3, 10])
    [f(5) for f in fs]  # [10, 15, 50]

    This is the classic LATE-BINDING pitfall: the naive
    `[lambda x: x * f for f in factors]` gives every lambda the LAST
    factor. Capture each factor at definition time (default argument,
    an inner factory function, functools.partial — your choice)."""
```

Edge cases the grader checks:

- Two counters advanced alternately keep separate counts.
- `make_accumulator()` with no argument starts from 0.
- `make_multipliers([])` returns `[]`; a single factor works; the
  functions remain correct when called repeatedly and out of order.
- The factories must not rely on global state (two calls to any
  factory never interfere).

Examples:

```python
>>> c1, c2 = make_counter(), make_counter()
>>> c1(), c1(), c2()
(1, 2, 1)
>>> acc = make_accumulator()
>>> acc(5), acc(-2)
(5, 3)
>>> [f(2) for f in make_multipliers([1, 2, 3])]
[2, 4, 6]
```
