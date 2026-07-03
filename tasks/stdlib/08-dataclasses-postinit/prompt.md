# Derived fields and vanishing init args

Two advanced dataclass moves: `__post_init__` runs after the generated
`__init__` (validate, compute derived fields), and `InitVar` declares a
constructor argument that is passed to `__post_init__` but never stored as
a field. In `solution.py`, define:

## 1. `Rectangle`

A dataclass with fields `width` and `height` (numbers), plus a derived
`area` attribute that is **computed, not passed in**:

- `Rectangle(3, 4).area == 12` — and `Rectangle(3, 4)` takes exactly two
  constructor arguments; passing `area` must be a `TypeError`.
- Construction validates: `width <= 0` or `height <= 0` raises
  `ValueError`.

(The intended shape: `area: int = field(init=False)` set inside
`__post_init__`.)

## 2. `User`

A dataclass whose constructor takes `name` and a plain-text `password`,
but which stores only a hash:

- `User("ada", "s3cret")` (also `User(name="ada", password="s3cret")`).
- `u.name == "ada"`; `u.password_hash` is the SHA-256 hex digest of the
  UTF-8 encoded password: `hashlib.sha256(b"s3cret").hexdigest()`.
- The plain password is **not stored**: `u` has no `password` attribute,
  and `repr(u)` must not contain `"s3cret"`.
- `check(u, attempt)` — module-level function returning `True` iff
  `attempt` is the password `u` was built with.

(The intended shape: `password: InitVar[str]`, hashed in
`__post_init__(self, password)`.)

Example:

```python
>>> r = Rectangle(3, 4)
>>> r.area
12
>>> Rectangle(0, 5)
ValueError: ...
>>> u = User("ada", "s3cret")
>>> hasattr(u, "password")
False
>>> check(u, "s3cret"), check(u, "guess")
(True, False)
```
