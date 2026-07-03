# A well-behaved @count_calls

In `solution.py`, write a plain function decorator:

```python
def count_calls(fn):
    """Decorator: the wrapped function works exactly like `fn`, and
    additionally carries a `.calls` attribute counting invocations."""
```

Required behaviour of the decorated function `wrapper = count_calls(fn)`:

- **Transparent**: any positional/keyword arguments are passed through;
  the return value comes back unchanged.
- **Counting**: `wrapper.calls` starts at 0 (before any call) and goes
  up by 1 for EVERY invocation — including calls that raise. The
  exception itself must propagate unchanged.
- **Metadata preserved** (this is what `functools.wraps` is for):
  - `wrapper.__name__` and `wrapper.__doc__` equal the original's;
  - `wrapper.__wrapped__` is the original function object (wraps sets
    this — it's how `inspect.unwrap` and debuggers find the real
    function).
- **Independent counters**: decorating two functions gives each its
  own `.calls`.

Example:

```python
@count_calls
def greet(name, punct="!"):
    """Say hi."""
    return f"hi {name}{punct}"

>>> greet.calls
0
>>> greet("bo"), greet("ada", punct="?")
('hi bo', 'hi ada?')
>>> greet.calls
2
>>> greet.__name__, greet.__doc__
('greet', 'Say hi.')
>>> greet.__wrapped__("x")   # the undecorated original
'hi x!'
```
