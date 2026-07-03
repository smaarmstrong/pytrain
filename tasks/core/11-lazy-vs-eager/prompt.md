# Eager list, lazy stream

Two functions in `solution.py` that do the same transformation with
opposite evaluation strategies — a list comprehension vs a generator
expression. The grader observes *when* your code consumes its input,
so only genuinely lazy/eager implementations pass.

```python
def eager_squares(nums) -> list:
    """Return a LIST of the squares of nums. The whole input is
    consumed before the function returns (that's what building a
    list means)."""

def lazy_squares(nums):
    """Return a LAZY iterator over the squares of nums.

    - Calling lazy_squares(...) must consume NOTHING from `nums`.
    - Each next() pulls exactly one more item from `nums`.
    - Works on unbounded inputs: taking 3 items from
      lazy_squares(itertools.count(1)) must terminate.
    - Like any iterator it is one-shot: once exhausted, it stays
      exhausted (next() raises StopIteration, list() gives []).
    """
```

Notes:

- `lazy_squares` is a one-line generator expression (`return (n*n for
  n in nums)`) or a generator function — either passes; returning a
  list (or otherwise pre-consuming the input) fails.
- `eager_squares` must return an actual `list`, fully populated at
  return time even if nobody ever looks at it.

Examples:

```python
>>> eager_squares([1, 2, 3])
[1, 4, 9]
>>> import itertools
>>> s = lazy_squares(itertools.count(1))   # infinite input: fine
>>> next(s), next(s), next(s)
(1, 4, 9)
>>> g = lazy_squares([2, 3])
>>> list(g), list(g)
([4, 9], [])
```
