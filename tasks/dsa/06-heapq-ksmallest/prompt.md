# K smallest, lazily

In `solution.py`, implement:

```python
def k_smallest(items, k):
    """Return the k smallest values of `items`, ascending.

    `items` is any iterable (possibly a one-shot generator, possibly huge —
    you may only iterate it ONCE and must not materialise it into a sorted
    list). k may exceed the number of items (return everything sorted) and
    may be 0 (return []).
    """
```

Requirements:

- Works on any one-pass iterable, not just lists.
- Returns a `list`, ascending order.
- Duplicates are kept: `k_smallest([2, 1, 2, 1], 3) == [1, 1, 2]`.
- Aim for O(k) memory, not O(n): the intended approach maintains "the k
  smallest so far" with the `heapq` module rather than sorting everything.
  The grader runs n = 500 000 under a time budget as a sanity check.

Examples:

```python
>>> k_smallest([5, 3, 9, 1, 4], 3)
[1, 3, 4]
>>> k_smallest(iter(range(1000, 0, -1)), 2)
[1, 2]
>>> k_smallest([], 5)
[]
```
