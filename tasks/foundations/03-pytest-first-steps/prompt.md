# Assert it: how this trainer grades you

Two things in `solution.py` — a tiny function, and a pytest-style test
for it:

```python
def divide(a: float, b: float) -> float:
    """a divided by b. divide(10, 2) -> 5.0"""

def test_divide():
    """Asserts that divide behaves: correct answers, and dividing by
    zero raises ZeroDivisionError."""
```

Behaviour details:

- `divide(a, b)` returns `a / b` (true division: `divide(10, 2)` is `5.0`,
  `divide(1, 4)` is `0.25`). Don't catch anything — dividing by zero should
  raise `ZeroDivisionError` naturally, like `/` does.
- `test_divide()` takes no arguments and uses plain `assert` statements to
  check **at least**:
  - `divide(10, 2) == 5.0`
  - `divide(1, 4) == 0.25`
  - `divide(1, 0)` raises `ZeroDivisionError` — the try/except pattern from
    the lesson: call it inside `try`, `assert False` if it returns, and
    `pass` in `except ZeroDivisionError`.
- The test must be a *real* test: it passes against your correct `divide`,
  and it must **fail (raise `AssertionError`) if `divide` were broken** —
  the grader checks this by secretly swapping in a wrong implementation and
  running your `test_divide` against it.

Examples:

```python
>>> divide(10, 2)
5.0
>>> test_divide()      # your divide is correct -> completes silently
```
