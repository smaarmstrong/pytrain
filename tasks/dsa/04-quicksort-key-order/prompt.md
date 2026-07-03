# Quicksort & custom key ordering

In `solution.py`, implement:

```python
def quicksort(items):
    """Return a NEW list with the elements of `items` ascending.

    Implement quicksort (or heapsort if you prefer) yourself — no
    `sorted()` / `.sort()`. `items` must not be mutated. Duplicates,
    already-sorted and reverse-sorted inputs all work.
    """

def sort_words(words):
    """Return a NEW list of `words` ordered by a custom key:

    1. shorter words first (ascending length),
    2. ties broken alphabetically, case-insensitively (use str.casefold),
    3. words that tie on BOTH keep their original relative order
       (i.e. the sort is stable).

    For this one, DO use Python's built-in sorting with `key=` — building
    the right key tuple is the exercise.
    """
```

Requirements:

- `quicksort` handles `[]`, single elements, all-equal lists, and inputs of
  a few thousand elements (pick pivots sensibly enough not to hit the
  recursion limit on sorted input — e.g. middle element or random pivot,
  seeded or not, since the *output* is deterministic either way).
- `sort_words` must not compare words case-sensitively for the alphabetical
  tie-break: `["b", "A"]` sorts to `["A", "b"]`.

Examples:

```python
>>> quicksort([3, 1, 2, 1])
[1, 1, 2, 3]
>>> sort_words(["pear", "Fig", "apple", "fig"])
['Fig', 'fig', 'pear', 'apple']
>>> sort_words(["b", "A", "ab"])
['A', 'b', 'ab']
```

(`"Fig"` stays before `"fig"`: same length, equal casefolded key, so the
original order is kept.)
