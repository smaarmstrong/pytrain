# Binary search three ways

In `solution.py`, implement:

```python
def binary_search(items, target):
    """items is a list sorted ascending (duplicates allowed).

    Return an index i with items[i] == target — any matching index is
    accepted when the target occurs more than once. Return -1 if absent.
    """

def insert_position(items, target):
    """items is a list sorted ascending (duplicates allowed).

    Return the LEFTMOST index at which target could be inserted while
    keeping items sorted (the bisect_left answer). For an empty list
    return 0.
    """

def search_rotated(nums, target):
    """nums is a sorted-ascending list of DISTINCT values that has been
    rotated by some pivot (possibly rotated by 0, i.e. still sorted),
    e.g. [4, 5, 6, 7, 0, 1, 2].

    Return the index of target, or -1 if absent. Empty list -> -1.
    """
```

Requirements:

- All three run in O(log n) — no linear scans (not timed, but write them as
  real binary searches; that is the point of the exercise).
- `insert_position` must match `bisect.bisect_left` exactly, including with
  duplicates and targets smaller/larger than everything.
- `search_rotated` must handle every rotation amount, including 0, and
  single-element lists.

Examples:

```python
>>> binary_search([1, 3, 5, 7], 5)
2
>>> binary_search([1, 3, 5, 7], 4)
-1
>>> insert_position([1, 3, 3, 5], 3)
1
>>> insert_position([], 42)
0
>>> search_rotated([4, 5, 6, 7, 0, 1, 2], 0)
4
>>> search_rotated([4, 5, 6, 7, 0, 1, 2], 3)
-1
```
