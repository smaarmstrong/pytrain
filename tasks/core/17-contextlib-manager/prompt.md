# Patch it back: @contextmanager

The previous task built a context manager the long way, with `__enter__`
and `__exit__`. `contextlib.contextmanager` turns a generator function
into one: code before `yield` runs on entry, the yielded value becomes
the `as` target, and code after the `yield` runs on exit. If the block
raises, the exception is thrown *into* the generator at the `yield` —
so cleanup belongs in `try/finally`, and catching an exception around
the `yield` suppresses it.

In `solution.py`, write two generator-based context managers (the
intended tool is `@contextlib.contextmanager`):

```python
@contextmanager
def patched(obj, name, value):
    """Temporarily set attribute `name` on `obj` to `value`."""

@contextmanager
def suppress_and_log(log, *exc_types):
    """Suppress exceptions of the given types, recording them in `log`."""
```

## `patched(obj, name, value)`

- On entry, sets `obj.name = value` and yields `obj`.
- On exit the attribute is put back exactly as it was:
  - if the attribute existed before, its previous value is restored;
  - if it did NOT exist before, it is removed again (`hasattr` is
    `False` afterwards).
- Restoration happens **even when the block raises**, and the
  exception still propagates out of the `with` block.
- Each call to `patched(...)` returns a fresh, independent context
  manager.

## `suppress_and_log(log, *exc_types)`

- `log` is a list; `exc_types` are exception classes.
- If the block raises an exception that is an instance of any of
  `exc_types` (subclasses count, like an `except` clause), the
  exception **object** is appended to `log` and the exception is
  suppressed — execution continues after the `with` block.
- Any other exception propagates unchanged and nothing is appended.
- On a clean exit nothing is appended.

Examples:

```python
>>> class Cfg: retries = 3
>>> cfg = Cfg()
>>> with patched(cfg, "retries", 10) as c:
...     print(c.retries)
10
>>> cfg.retries
3

>>> log = []
>>> with suppress_and_log(log, ValueError):
...     raise ValueError("bad input")
>>> len(log), str(log[0])
(1, 'bad input')
```
