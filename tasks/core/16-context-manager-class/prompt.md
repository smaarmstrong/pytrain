# Rollback: a transactional context manager

In `solution.py`, write a CLASS-based context manager (explicit
`__enter__` and `__exit__` — no `contextlib` here; the next task covers
that) that makes edits to a dict transactional.

```python
class Rollback:
    def __init__(self, data: dict, swallow: bool = False):
        """Wrap `data`. `swallow` controls exception propagation."""
```

Behaviour:

- `__enter__` snapshots the dict's current contents (a shallow copy is
  fine — treat values as atomic) and returns the SAME dict object, so
  `with Rollback(d) as d2:` gives `d2 is d`.
- **Clean exit**: all changes made inside the block are kept.
- **Exception inside the block**: the dict is restored to its snapshot
  — added keys removed, deleted keys reinstated, changed values
  reverted. Then:
  - `swallow=False` (default): the exception propagates out of the
    `with` block (`__exit__` returns a falsy value).
  - `swallow=True`: the exception is suppressed (`__exit__` returns
    True) and execution continues after the block.
- The three `__exit__` arguments (`exc_type, exc, tb`) are `None` on a
  clean exit — that's how you tell the cases apart.
- A single `Rollback` instance may be reused in a second `with`
  statement (each entry takes a fresh snapshot).

Examples:

```python
>>> d = {"a": 1}
>>> with Rollback(d) as d2:
...     d2["b"] = 2
>>> d
{'a': 1, 'b': 2}

>>> d = {"a": 1}
>>> try:
...     with Rollback(d):
...         d["a"] = 99
...         d["junk"] = True
...         raise RuntimeError("boom")
... except RuntimeError:
...     pass
>>> d
{'a': 1}

>>> d = {"a": 1}
>>> with Rollback(d, swallow=True):
...     del d["a"]
...     raise ValueError("no matter")
>>> d          # rolled back, exception swallowed
{'a': 1}
```
