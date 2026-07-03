# Stars and slashes

Three functions in `solution.py` exercising unpacking and parameter kinds.

```python
def head_tail(seq):
    """Split a sequence into (first, middle, last) where `middle` is a
    list of everything in between. Raise ValueError if len(seq) < 2.
    head_tail([1, 2, 3, 4]) == (1, [2, 3], 4)
    head_tail("ab") == ("a", [], "b")
    Hint: starred assignment does this in one line."""

def merge(*dicts, **overrides):
    """Merge any number of dicts left to right (later dicts win), then
    apply keyword overrides on top (they win over everything). Return a
    NEW dict; never mutate the arguments.
    merge({"a": 1}, {"a": 2, "b": 3}, a=9) == {"a": 9, "b": 3}
    merge() == {}."""

def clamp(value, /, lo, hi, *, strict=False):
    """Clamp `value` into [lo, hi].

    - `value` is POSITIONAL-ONLY: clamp(value=5, lo=0, hi=9) must raise
      TypeError (the standard error for a bad call — do not raise it
      yourself, declare the parameter positional-only).
    - `strict` is KEYWORD-ONLY: clamp(5, 0, 9, True) must raise TypeError.
    - lo/hi may be given positionally or by keyword.
    - With strict=True, raise ValueError if value is outside [lo, hi]
      instead of clamping.
    """
```

Examples:

```python
>>> head_tail(("x", "y", "z"))
('x', ['y'], 'z')
>>> merge({"host": "a"}, {"port": 1}, port=8080)
{'host': 'a', 'port': 8080}
>>> clamp(15, 0, 10)
10
>>> clamp(15, lo=0, hi=10, strict=True)
Traceback (most recent call last):
...
ValueError: ...
```
