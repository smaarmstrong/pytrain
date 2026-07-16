# Read the traceback, fix the bug

`solution.py` contains three small functions. Each one crashes when called.
Your job is not to rewrite them — it is to **run them, read each traceback,
and make the one-line fix it points at**.

```python
def greet(name: str) -> str:
    """greet("Bo") -> "Hello, Bo!" """

def label_age(age: int) -> str:
    """label_age(7) -> "age: 7" """

def last(items: list):
    """last([3, 1, 4]) -> 4 — the final element."""
```

Behaviour details:

- `greet("Bo")` returns `"Hello, Bo!"` — currently it raises `NameError`.
- `label_age(7)` returns `"age: 7"` — currently it raises `TypeError`.
- `last([3, 1, 4])` returns `4` — currently it raises `IndexError`, for
  every non-empty list.
- Each fix is one line. The file already has a `demo` section at the bottom
  guarded by `if __name__ == "__main__":` so that running
  `python3 solution.py` calls each function and shows you the crash —
  uncomment one call at a time, run, read the traceback bottom-up, fix.

Examples:

```python
>>> greet("Bo")
'Hello, Bo!'
>>> label_age(7)
'age: 7'
>>> last([3, 1, 4])
4
```
