# 2-D dynamic programming: grids, edits, subsequences

Three classics where the table has two dimensions. In `solution.py`,
implement:

```python
def grid_paths(rows, cols, blocked=()):
    """Count the paths from the top-left cell (0, 0) to the bottom-right
    cell (rows-1, cols-1) of a rows x cols grid, moving only RIGHT or
    DOWN, never entering a blocked cell.

    - rows, cols >= 1.
    - `blocked` is an iterable of (r, c) tuples; coordinates outside the
      grid may appear and are simply irrelevant.
    - If (0, 0) or (rows-1, cols-1) is blocked -> 0.
    - grid_paths(1, 1) == 1 (you are already there).
    - Counts are exact ints and get big: grid_paths(18, 18) is
      2333606220 — pure recursion won't finish, a table will.
    """

def edit_distance(a, b):
    """Levenshtein distance between strings a and b: the minimum number
    of single-character INSERTS, DELETES and SUBSTITUTIONS turning a
    into b.

    edit_distance("kitten", "sitting") == 3
    edit_distance("", x) == len(x); identical strings -> 0.
    """

def lcs_length(a, b):
    """Length of the longest common SUBSEQUENCE of strings a and b
    (characters in order, not necessarily contiguous).

    lcs_length("abcde", "ace") == 3        # "ace"
    lcs_length("abc", "xyz") == 0
    Either string empty -> 0.
    """
```

Requirements:

- All three must handle inputs around 200 per dimension promptly (strings
  of length 200, an 80 x 80 grid) — that's ~40 000 table cells, instant
  for a real DP, hopeless for un-memoised recursion.
- Exact integers everywhere; no floating point.
- Do not import difflib or similar — build the tables yourself.

Examples:

```python
>>> grid_paths(3, 3)
6
>>> grid_paths(3, 3, blocked={(1, 1)})
2
>>> edit_distance("flaw", "lawn")
2
>>> lcs_length("AGGTAB", "GXTXAYB")
4
```
