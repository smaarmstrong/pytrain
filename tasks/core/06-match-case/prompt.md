# Command dispatcher

In `solution.py`, implement a single function that interprets loosely
structured "drawing commands". The shapes involved (tuples of varying
length, nested tuples, mappings, guards, catch-all) are exactly what
`match`/`case` structural pattern matching is for — write it as one
`match` statement.

```python
def dispatch(cmd) -> str:
    """Interpret one command and return a description string."""
```

Rules, checked top to bottom (first match wins):

| command shape | return value |
|---|---|
| `("quit",)` | `"quit"` |
| `("move", x, y)` where x and y are both ints **and** both >= 0 | `"move to (x, y)"` e.g. `"move to (3, 4)"` |
| `("move", x, y)` with any other x/y | `"invalid move"` |
| `("line", (x1, y1), (x2, y2))` — two 2-tuples/2-lists of anything | `"line from (x1, y1) to (x2, y2)"` |
| a dict with `"action"` key equal to `"set"` and keys `"key"`, `"value"` | `"set <key>=<value!r>"` e.g. `"set colour='red'"` |
| any other non-empty list/tuple | `"sequence of N"` where N is its length |
| a plain string `s` | `"text: s"` e.g. `"text: hello"` |
| anything else (incl. empty tuple/list, numbers, None, dicts without the shape above) | `"unknown"` |

Notes:

- A string must hit the string rule, **not** the sequence rule, even
  though strings are sequences (`match` sequence patterns already
  exclude `str` — if you don't use `match`, you must handle this).
- The dict rule must tolerate extra keys:
  `{"action": "set", "key": "k", "value": 1, "who": "me"}` still matches.
- `("move", 1.5, 2)` (floats) → `"invalid move"`; note that `match`
  int-checking treats `True` as an int — the grader does not test bools.

Examples:

```python
>>> dispatch(("move", 3, 4))
'move to (3, 4)'
>>> dispatch(("line", (0, 0), (2, 5)))
'line from (0, 0) to (2, 5)'
>>> dispatch({"action": "set", "key": "colour", "value": "red"})
"set colour='red'"
>>> dispatch([10, 20, 30, 40])
'sequence of 4'
>>> dispatch("hello")
'text: hello'
>>> dispatch(None)
'unknown'
```
