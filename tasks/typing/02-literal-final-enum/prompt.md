# Literal, Final and enums in signatures

In `solution.py`, write a tiny "job runner" vocabulary that puts three typing
tools to work: `Literal`, `Final` and an `Enum`.

```python
MAX_RETRIES: Final[int] = 3          # module-level constant, annotated Final[int]

class Status(enum.Enum):             # exactly these three members
    OK = "ok"
    WARN = "warn"
    ERROR = "error"

def set_mode(mode: Literal["r", "w", "a"]) -> str:
    """Return 'mode set to <mode>'. Raise ValueError for any other string."""

def severity(status: Status) -> int:
    """OK -> 0, WARN -> 1, ERROR -> 2. Parameter annotated as Status."""
```

Requirements:

- `MAX_RETRIES` must be annotated `Final[int]` (the grader reads the module's
  resolved type hints) and equal `3`.
- `set_mode`'s parameter must be annotated with a `Literal` of exactly the
  three strings `"r"`, `"w"`, `"a"`; at runtime any other value raises
  `ValueError`.
- `severity`'s parameter must be annotated with your `Status` enum, and its
  return with `int`.

Examples:

```python
>>> set_mode("w")
'mode set to w'
>>> set_mode("x")
Traceback (most recent call last):
ValueError: ...
>>> severity(Status.WARN)
1
```
