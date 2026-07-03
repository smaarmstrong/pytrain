# Callable types and a ParamSpec retry decorator

A decorator that wraps *any* function can't describe its signature with plain
`Callable[..., R]` without throwing the parameter types away. `ParamSpec`
captures the full parameter list so the wrapped function keeps its exact
signature. In `solution.py`:

1. A plain `Callable`-typed higher-order function:

```python
def apply_twice(fn: Callable[[int], int], value: int) -> int:
    """fn(fn(value))."""
```

2. A retry decorator factory typed with `ParamSpec`:

```python
P = ParamSpec("P")
R = TypeVar("R")

def retry(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """@retry(times) wraps a function so it is called up to `times` times:
    the first successful call's result is returned; if every attempt raises,
    the LAST exception propagates. `times` >= 1.

    - all positional and keyword arguments must be forwarded unchanged
    - metadata must be preserved with functools.wraps
    """
```

(PEP 695 spelling `def retry[**P, R](times: int) -> ...` is also accepted —
either way, a `ParamSpec` must be involved; the grader checks for one.)

Examples:

```python
>>> apply_twice(lambda x: x + 3, 10)
16

>>> calls = 0
>>> @retry(3)
... def flaky():
...     global calls; calls += 1
...     if calls < 3: raise OSError("boom")
...     return "ok"
>>> flaky()
'ok'
>>> flaky.__name__
'flaky'
```
