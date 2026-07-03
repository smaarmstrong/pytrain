# An enum toolkit

In `solution.py`, define three enums and one helper (Python 3.11+,
`from enum import ...`):

1. `Priority(IntEnum)` with members `LOW = 1`, `MEDIUM = 2`, `HIGH = 3`.
   Being an `IntEnum`, members compare and mix with plain ints:
   `Priority.HIGH > 2`, `sorted(...)` works, `Priority(3) is Priority.HIGH`.

2. `Color(StrEnum)` with members `RED`, `GREEN`, `BLUE` declared with
   `auto()`, so their values are the lowercase names `"red"`, `"green"`,
   `"blue"`. Being a `StrEnum`: `Color.RED == "red"`,
   `str(Color.GREEN) == "green"`, `Color("blue") is Color.BLUE`, and string
   methods work (`Color.RED.upper() == "RED"`).

3. `Permission(Flag)` with members `READ`, `WRITE`, `EXECUTE` declared with
   `auto()`. Members combine with `|` and support membership tests:
   `Permission.READ in (Permission.READ | Permission.WRITE)`.

4. A function:

```python
def parse_permissions(names):
    """Combine an iterable of permission names, case-insensitively, into a
    single Permission value.

    parse_permissions(["read", "WRITE"]) == Permission.READ | Permission.WRITE
    parse_permissions([]) == Permission(0)
    Unknown names raise ValueError.
    """
```

Examples:

```python
>>> Priority.LOW < Priority.HIGH
True
>>> Color.RED == "red"
True
>>> parse_permissions(["Execute"]) is Permission.EXECUTE
True
>>> parse_permissions(["admin"])
ValueError: ...
```
