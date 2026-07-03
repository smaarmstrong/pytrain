# Shapes behind an ABC

In `solution.py`, implement an abstract base class and two concrete shapes:

```python
from abc import ABC, abstractmethod

class Shape(ABC): ...
class Rectangle(Shape): ...   # Rectangle(width, height)
class Circle(Shape): ...      # Circle(radius)
```

Behaviour:

- `Shape` declares **abstract** methods `area(self)` and `perimeter(self)`.
  Consequently:
  - `Shape()` raises `TypeError`;
  - any subclass that fails to implement *both* methods also raises
    `TypeError` when instantiated.
- `Shape` provides one **concrete** method, inherited by every subclass:

  ```python
  def describe(self):
      # exactly this format, two decimal places:
      # "<ClassName>: area=<area>, perimeter=<perimeter>"
  ```

  e.g. `"Rectangle: area=12.00, perimeter=14.00"`. It must call the
  subclass's `area()`/`perimeter()`, and use the *runtime* class name — a
  grader-defined subclass `Tri` describes itself as `"Tri: ..."`.
- `Rectangle(width, height)`: `area() == width * height`,
  `perimeter() == 2 * (width + height)`.
- `Circle(radius)`: `area() == math.pi * r**2`,
  `perimeter() == 2 * math.pi * r`.

Examples:

```python
>>> Rectangle(3, 4).describe()
'Rectangle: area=12.00, perimeter=14.00'
>>> Shape()
TypeError: ...
```
