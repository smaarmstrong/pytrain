# Merge sort, stably

In `solution.py`, implement merge sort yourself (no `sorted()` / `.sort()` —
the grader can't see your code, but you'd only be cheating yourself):

```python
def merge(left, right, key=None):
    """Merge two already-sorted lists into one sorted list.

    When elements compare equal, elements of `left` come before elements
    of `right` (this is what makes the overall sort stable).
    """

def merge_sort(items, key=None):
    """Return a NEW list with the elements of `items` in ascending order.

    - `items` must NOT be mutated.
    - If `key` is given, order by key(x); otherwise by the elements
      themselves.
    - The sort must be STABLE: elements that compare equal keep their
      original relative order.
    """
```

Requirements:

- Handles empty lists, single elements, all-equal lists and duplicates.
- With `key=` the elements themselves are never compared, only their keys —
  the grader sorts dicts (which don't support `<`) by a key function.
- Stability is tested: `merge_sort([(2,'a'),(1,'b'),(2,'c')], key=lambda t: t[0])`
  must give `[(1,'b'),(2,'a'),(2,'c')]` — `(2,'a')` stays before `(2,'c')`.

Examples:

```python
>>> merge([1, 4], [2, 3])
[1, 2, 3, 4]
>>> merge_sort([5, 3, 1, 4, 2])
[1, 2, 3, 4, 5]
>>> merge_sort(["bb", "a", "ccc"], key=len)
['a', 'bb', 'ccc']
```
