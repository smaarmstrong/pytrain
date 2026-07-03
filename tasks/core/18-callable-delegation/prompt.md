# Callables and a logging proxy

Two small classes in `solution.py` exercise two dunder hooks:
`__call__` makes an *instance* callable like a function, and
`__getattr__` is invoked only when normal attribute lookup fails —
which makes it the tool for transparent delegation to a wrapped object.

```python
class RunningMean:
    """A callable accumulator."""
    def __init__(self): ...

class LoggingProxy:
    """Wraps any object; delegates attribute reads and records them."""
    def __init__(self, target): ...
```

## `RunningMean`

- Instances are callable. Each call takes one number and returns the
  arithmetic mean of **all values fed so far**, as a `float` (true
  division — `rm(1); rm(2)` returns `1.5`, not `1`).
- `rm.count` is the number of calls made so far (an `int`, starts at 0).
- Separate instances accumulate independently.

## `LoggingProxy`

- `LoggingProxy(target)` wraps any object.
- Reading an attribute that the proxy itself doesn't have is delegated
  to `target`: `proxy.append` gives you the target list's bound
  `append`, `proxy.colour` gives you the target's `colour` value.
- `proxy.accessed` is a list of the attribute **names** successfully
  delegated, in order, duplicates included. It is the proxy's own
  attribute: reading `accessed` must not record anything.
- If `target` has no such attribute either, `AttributeError` is raised
  and nothing is recorded.

Hint: `__getattr__` (not `__getattribute__`) only fires when the normal
lookup misses, so the proxy's own attributes set in `__init__` are found
first and never delegated.

Examples:

```python
>>> rm = RunningMean()
>>> rm(10), rm(20), rm.count
(10.0, 15.0, 2)

>>> items = [1, 2]
>>> p = LoggingProxy(items)
>>> p.append(3)
>>> items
[1, 2, 3]
>>> p.accessed
['append']
```
