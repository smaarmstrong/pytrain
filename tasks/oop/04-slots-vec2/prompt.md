# Vec2 on a diet: `__slots__`

In `solution.py`, implement a slotted 2-D vector:

```python
class Vec2:
    def __init__(self, x, y): ...
```

Behaviour:

- `v.x` and `v.y` are readable **and writable**.
- The class declares `__slots__` so instances carry *only* `x` and `y`:
  - setting any other attribute (`v.z = 1`, `v.colour = "red"`) raises
    `AttributeError`;
  - instances have no `__dict__` (`hasattr(v, "__dict__")` is `False`).
- Value equality: `Vec2(1, 2) == Vec2(1, 2)` is `True`,
  `Vec2(1, 2) == Vec2(1, 3)` is `False`, and comparing with a non-`Vec2`
  (e.g. the tuple `(1, 2)`) is `False`, not an error.
- `repr(Vec2(1, 2))` is exactly `"Vec2(1, 2)"` (each coordinate rendered
  with `repr`).
- `v.translated(dx, dy)` returns a **new** `Vec2` shifted by `(dx, dy)`;
  the original is unchanged.

Examples:

```python
>>> v = Vec2(1, 2)
>>> v.translated(3, -1)
Vec2(4, 1)
>>> v.z = 9
AttributeError: ...
```
