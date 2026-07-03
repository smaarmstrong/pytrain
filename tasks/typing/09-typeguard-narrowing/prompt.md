# Narrowing with isinstance and TypeGuard

Static checkers *narrow* a value's type when they can prove something about
it: after `isinstance(x, str)`, `x` is a `str`. You can teach mypy new
narrowing rules with `TypeGuard` (or `TypeIs` on 3.13+). In `solution.py`:

```python
def is_str_list(items: list[object]) -> TypeGuard[list[str]]:
    """True iff every element is a str. An empty list counts as True.
    The return annotation must be TypeGuard[list[str]] (or TypeIs[...]),
    so that mypy narrows `items` to list[str] in the True branch."""

def join_upper(items: list[object]) -> str:
    """If is_str_list(items): the elements upper-cased, joined with '-'.
    Otherwise raise TypeError."""

def describe(value: int | str | list[object]) -> str:
    """Use isinstance narrowing:
    int   -> 'number <value>'
    str   -> 'text <value>'
    list  -> 'list of <len> items'
    """
```

Examples:

```python
>>> is_str_list(["a", "b"])
True
>>> is_str_list(["a", 1])
False
>>> join_upper(["a", "b"])
'A-B'
>>> describe(7)
'number 7'
>>> describe([1, 2])
'list of 2 items'
```

Grading: behaviour, mypy clean on your module (`--disallow-untyped-defs`),
and a grader snippet that checks the narrowing really happens:

```python
def check(v: list[object]) -> None:
    if is_str_list(v):
        assert_type(v, list[str])   # must type-check
```
