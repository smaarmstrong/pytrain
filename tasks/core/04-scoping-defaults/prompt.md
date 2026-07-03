# Fresh lists and counters

Three functions in `solution.py` that only work if you understand where
Python looks names up (LEGB: Local, Enclosing, Global, Built-in) and why
`def f(x, items=[])` is a famous bug.

```python
def append_item(item, items=None) -> list:
    """Append `item` to `items` and return the list.

    - If `items` is given, mutate and return that very list.
    - If omitted, use a FRESH empty list for this call. Two calls
      without `items` must NOT share state:
        append_item(1) == [1]
        append_item(2) == [2]      # not [1, 2]!
    """

def next_id() -> int:
    """Return 1, then 2, then 3, ... on successive calls.

    The counter lives at MODULE level (a global), so independent
    callers share the same sequence. You'll need the `global`
    statement (or a module-level mutable) to rebind it."""

def make_prefixer(prefix: str):
    """Return a function f(s) -> prefix + s. The returned function
    reads `prefix` from the enclosing scope:
        shout = make_prefixer(">> ")
        shout("hi") == ">> hi"
    Later calls to make_prefixer must not disturb earlier prefixers."""
```

Edge cases the grader checks:

- `append_item("x", existing)` returns `existing` itself (same object),
  now one longer.
- Interleaving: `f = make_prefixer("a-"); g = make_prefixer("b-")` —
  `f("x") == "a-x"` and `g("x") == "b-x"` in any call order.
- `next_id` starts at 1 for a freshly imported module.

Examples:

```python
>>> append_item(5)
[5]
>>> append_item(6)
[6]
>>> bucket = ["a"]
>>> append_item("b", bucket) is bucket
True
>>> next_id(), next_id(), next_id()
(1, 2, 3)
```
