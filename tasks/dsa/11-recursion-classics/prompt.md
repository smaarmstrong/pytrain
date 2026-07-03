# Recursion classics: permutations, subsets, flatten

Three problems that recursion solves cleanly. In `solution.py`, implement:

```python
def permutations_of(items):
    """Return ALL orderings of `items` as a list of lists.

    `items` is a list (length <= 7). Treat positions as distinct even if
    values repeat: permutations_of([1, 1]) has 2 entries, [[1, 1], [1, 1]].
    The result therefore always has exactly n! entries.
    The ORDER of the permutations in the result does not matter.
    permutations_of([]) == [[]] (one empty ordering).
    """

def subsets_of(items):
    """Return every subset of `items` as a list of lists.

    `items` is a list of DISTINCT values (length <= 10). Each subset must
    keep the elements in their original relative order, so each subset of
    [1, 2, 3] containing 1 and 3 is written [1, 3], never [3, 1].
    The result has exactly 2**n entries, including [] and the full list.
    The ORDER of the subsets in the result does not matter.
    """

def flatten(nested):
    """Flatten arbitrarily nested lists into one flat list, left to right.

    Only `list` instances are flattened; every other value (ints, strings,
    tuples, None, ...) is kept as an atom. Strings are atoms — never
    iterate into them. Empty lists contribute nothing.

    flatten([1, [2, [3, [4]]], 5]) == [1, 2, 3, 4, 5]
    flatten([]) == []
    flatten([[], [[]]]) == []
    """
```

Requirements:

- Do not use `itertools.permutations` / `itertools.combinations` — writing
  the recursion is the exercise (the grader can't see your code, but you'd
  only be cheating yourself).
- `flatten` must handle nesting at least 150 levels deep and must preserve
  the left-to-right order of atoms.
- None of the three may mutate their input.

Examples:

```python
>>> sorted(permutations_of([1, 2]))
[[1, 2], [2, 1]]
>>> sorted(subsets_of([1, 2]))
[[], [1], [1, 2], [2]]
>>> flatten(["ab", [1, ("x",)], []])
['ab', 1, ('x',)]
```
