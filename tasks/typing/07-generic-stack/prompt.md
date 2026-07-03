# A generic Stack[T]

In `solution.py`, implement a LIFO stack that is *generic over its element
type*: `Stack[int]` holds ints, and mypy must know that `pop()` on a
`Stack[int]` returns `int` — and must reject pushing a `str` onto it.

Use classic `Generic[T]` with a `TypeVar`; PEP 695 `class Stack[T]:` is also
accepted if your interpreter has it.

```python
class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...          # raises IndexError when empty
    def peek(self) -> T: ...         # raises IndexError when empty
    def is_empty(self) -> bool: ...
    def __len__(self) -> int: ...
```

Behaviour:

- `Stack()` starts empty; `push`/`pop` are LIFO; `peek` returns the top
  without removing it.
- `pop`/`peek` on an empty stack raise `IndexError`.
- `Stack[int]` must be subscriptable at runtime too (Generic gives you this
  for free).

Example:

```python
>>> s: Stack[int] = Stack()
>>> s.push(1); s.push(2)
>>> s.pop(), s.peek(), len(s)
(2, 1, 1)
```

Grading: behaviour, mypy clean on your module (`--disallow-untyped-defs`),
a snippet asserting `assert_type(s.pop(), int)` for a `Stack[int]` must
type-check, and a snippet pushing `"oops"` onto a `Stack[int]` must be
REJECTED by mypy.
