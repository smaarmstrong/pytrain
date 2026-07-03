# Set craft: dedupe, intersect, unique windows

In `solution.py`, implement:

```python
def dedupe(items):
    """Return a NEW list with duplicates removed, keeping only the FIRST
    occurrence of each value and preserving that original order.
    dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]. Items are hashable."""

def common_elements(a, b):
    """Return a sorted list of the DISTINCT values that appear in both
    lists. Duplicates within a list don't matter; each shared value
    appears once. Either list may be empty -> []."""

def first_unique_window(items, k):
    """Return the smallest index i such that the window items[i:i+k]
    contains k DISTINCT values (no repeats inside the window), or -1 if
    no such window exists.

    - k <= 0: raise ValueError.
    - k > len(items): return -1.
    - Aim for a sliding window with a set/dict of counts rather than
      re-checking every window from scratch (not timed, but that's the
      technique being practised).
    """
```

Examples:

```python
>>> dedupe([3, 1, 3, 2, 1])
[3, 1, 2]
>>> common_elements([4, 2, 2, 1], [2, 4, 4, 9])
[2, 4]
>>> first_unique_window([1, 2, 2, 3, 4, 5], 3)
2                      # [2, 3, 4] is the first all-distinct window of size 3
>>> first_unique_window([1, 1, 1], 2)
-1
>>> first_unique_window([7], 1)
0
```
