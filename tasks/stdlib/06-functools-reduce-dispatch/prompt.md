# Fold it, dispatch it

Two more `functools` power tools: `reduce` folds a sequence down to one
value, and `singledispatch` turns a plain function into one that picks an
implementation by the type of its first argument. In `solution.py`:

```python
def product_of(nums):
    """The product of all numbers in `nums`. Empty input -> 1."""

def compose(*funcs):
    """Compose one-argument functions, right to left.

    compose(f, g, h)(x) == f(g(h(x))). compose() is the identity function.
    """

def describe(value):
    """A one-line description of `value`, chosen by its type:

    - int   -> "int:<value>"          e.g. describe(5)      == "int:5"
    - str   -> "str:<value>"          e.g. describe("hi")   == "str:hi"
    - list  -> "list:<length>"        e.g. describe([1, 2]) == "list:2"
    - anything else -> "other:<type name>"   e.g. describe(3.5) == "other:float"

    `describe` must be EXTENSIBLE the way functools.singledispatch makes it:
    callers can register a handler for a new type with

        describe.register(SomeType, handler_function)

    and afterwards describe(instance_of_SomeType) — including instances of
    SUBCLASSES of SomeType — must use that handler.
    """
```

Examples:

```python
>>> product_of([2, 3, 4])
24
>>> add1 = lambda x: x + 1
>>> dbl = lambda x: x * 2
>>> compose(add1, dbl)(3)      # add1(dbl(3))
7
>>> describe([10, 20, 30])
'list:3'
>>> class Point: pass
>>> describe.register(Point, lambda p: "a point")
<function ...>
>>> describe(Point())
'a point'
```
