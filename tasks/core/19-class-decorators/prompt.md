# add_repr and singleton

A decorator can take a *class*, too: `@deco` above `class C:` runs
`C = deco(C)`. The decorator may modify the class and hand it back, or
return something else entirely that stands in for it. Write one of
each in `solution.py`:

```python
def add_repr(cls):
    """Class decorator: give `cls` a useful __repr__, return the class."""

def singleton(cls):
    """Class decorator: at most one instance of `cls` ever exists."""
```

## `add_repr(cls)`

- Returns the class it was given, with `__repr__` replaced.
- `repr(instance)` becomes `ClassName(attr1=value1, attr2=value2)`:
  the class's name, then each **instance** attribute as `name=value`
  in the order the attributes were set, comma-space separated, with
  each value rendered by `repr()` (so strings get quotes).
- An instance with no attributes reprs as `ClassName()`.
- The class must otherwise behave as before (construction, methods,
  existing attributes untouched).

## `singleton(cls)`

- The decorated name is still called the same way, but the underlying
  class is instantiated **at most once**:
  - Nothing is instantiated at decoration time (lazy).
  - The first call constructs the instance, passing through any
    arguments.
  - Every later call returns the SAME object (`is`), without running
    `__init__` again — later arguments are ignored.
- The returned object is a real instance of the original class
  (`isinstance` holds).
- Decorating two different classes gives two independent singletons.

Examples:

```python
>>> @add_repr
... class Point:
...     def __init__(self, x, y):
...         self.x = x
...         self.y = y
>>> repr(Point(1, 2))
'Point(x=1, y=2)'

>>> @singleton
... class Config:
...     def __init__(self, env="dev"):
...         self.env = env
>>> a = Config("prod")
>>> b = Config("ignored")
>>> a is b, a.env
(True, 'prod')
```
