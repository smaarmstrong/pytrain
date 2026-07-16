# See inside a running program

`solution.py` has two functions that run without crashing but return the
**wrong answers** — no traceback to help you this time. Find each bug by
looking inside the loop (print-debugging or `breakpoint()`, your choice)
and fix it.

```python
def running_total(nums: list) -> list:
    """running_total([1, 2, 3]) -> [1, 3, 6] — each element is the sum
    so far."""

def count_vowels(word: str) -> int:
    """count_vowels("debug") -> 2 — how many of a, e, i, o, u appear
    (lowercase input)."""
```

Behaviour details:

- `running_total([1, 2, 3])` returns `[1, 3, 6]`; `running_total([5])`
  returns `[5]`; `running_total([])` returns `[]`. Currently it returns
  `[1, 2, 3]` — the total isn't accumulating.
- `count_vowels("debug")` returns `2`; `count_vowels("rhythm")` returns
  `0`; `count_vowels("")` returns `0`. Currently it counts exactly the
  wrong letters.
- Each fix is one line. Resist re-writing from scratch: the exercise is to
  *observe* the wrong values as the loop runs, spot the moment reality
  diverges from your expectation, and correct that line. Remove any print
  calls you added before grading.

Examples:

```python
>>> running_total([1, 2, 3])
[1, 3, 6]
>>> count_vowels("debug")
2
```
