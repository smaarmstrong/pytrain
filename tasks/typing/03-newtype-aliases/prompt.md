# NewType and type aliases

In `solution.py`, build the typed vocabulary for a tiny user store.

1. A distinct id type:

```python
UserId = NewType("UserId", int)

def make_user_id(raw: int) -> UserId:
    """Validate raw > 0 and return it as a UserId; else raise ValueError."""
```

2. A type alias `Vector` for `list[float]`. On Python 3.12+ prefer the
   `type` statement; `Vector: TypeAlias = list[float]` (or a plain
   assignment) is also accepted:

```python
type Vector = list[float]

def scale(v: Vector, k: float) -> Vector:
    """Return a NEW list with every element multiplied by k (don't mutate v)."""
```

3. A lookup that speaks in `UserId`:

```python
def lookup(names: dict[UserId, str], uid: UserId) -> str | None:
    """The user's name, or None when uid is unknown."""
```

Behaviour requirements:

- `make_user_id(7)` returns `7` (NewType is erased at runtime — the value is
  still a plain `int`); `make_user_id(0)` and `make_user_id(-3)` raise
  `ValueError`.
- `scale([1.0, 2.5], 2.0) == [2.0, 5.0]` and the input list is unchanged.
- `lookup({UserId(1): "ada"}, UserId(1)) == "ada"`;
  `lookup({}, UserId(1)) is None`.

The grader checks that `UserId` really is a `NewType` over `int` and that
`Vector` really aliases `list[float]`.
