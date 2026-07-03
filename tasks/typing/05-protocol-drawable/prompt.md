# Structural typing with Protocol

In `solution.py`, define a protocol and implement it *structurally* — no
inheritance from the protocol allowed.

```python
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...


class Circle:
    """Circle(radius). draw() -> 'circle(r=<radius>)'"""

class Square:
    """Square(side). draw() -> 'square(s=<side>)'"""


def render_all(items: Iterable[Drawable]) -> list[str]:
    """Call .draw() on each item, in order."""
```

Requirements:

- `Drawable` is a `typing.Protocol` with a single method `draw(self) -> str`,
  decorated `@runtime_checkable` so `isinstance(x, Drawable)` works.
- `Circle` and `Square` must NOT list `Drawable` (or any other base) as a base
  class — the whole point is that they satisfy it by shape alone. Any class
  with a `draw() -> str` method must be accepted by `render_all`, including
  classes the grader defines itself.
- `render_all` must be annotated to accept an iterable of `Drawable` (the
  grader runs mypy on a snippet passing `[42]` and expects mypy to REJECT it,
  and on a snippet passing a structural third-party class and expects mypy to
  ACCEPT it).
- mypy must also be clean on your module with `--disallow-untyped-defs`.

Example:

```python
>>> render_all([Circle(2), Square(3)])
['circle(r=2)', 'square(s=3)']
>>> isinstance(Circle(1), Drawable)
True
```
