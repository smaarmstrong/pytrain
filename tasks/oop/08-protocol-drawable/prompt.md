# Drawable: structural typing at runtime

In `solution.py`, define a runtime-checkable protocol and a function that
uses it:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

def draw_all(items): ...
```

Behaviour:

- `Drawable` is **structural**: `isinstance(obj, Drawable)` is `True` for
  any object whose class has a `draw` method — no inheritance from
  `Drawable` required — and `False` for objects without one. (It must be
  decorated `@runtime_checkable`, otherwise `isinstance` refuses to work
  at all.)
- Like all protocols, `Drawable()` raises `TypeError`.
- `draw_all(items)` takes an iterable of objects and returns the list
  `[item.draw() for item in items]`, in order — **but** it first checks
  every item with `isinstance(..., Drawable)` and raises `TypeError` if any
  item does not conform, *before calling `draw()` on anything*.
- `draw_all([])` returns `[]`.

Examples:

```python
>>> class Square:                      # note: no base class
...     def draw(self): return "square"
>>> isinstance(Square(), Drawable)
True
>>> draw_all([Square(), Square()])
['square', 'square']
>>> draw_all([Square(), 42])
TypeError: ...
```
