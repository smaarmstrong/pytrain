# NumPy: build, reshape, slice

In `solution.py` (with `import numpy as np`), implement four small functions.
No Python loops are *required* anywhere — each is a one- or two-liner with
array creation, reshaping, slicing or fancy indexing.

```python
def make_grid(rows, cols):
    """A 2-D float array of shape (rows, cols) counting 0, 1, 2, ... row by row.

    dtype must be a floating dtype (float64 is fine).
    """

def checkerboard(n):
    """An n x n INTEGER array where cell [i, j] == (i + j) % 2.

    So the top-left cell is 0 and colours alternate in both directions.
    Hint: start from zeros and use slice assignment with step 2.
    """

def every_other_row_reversed(a):
    """Rows 0, 2, 4, ... of 2-D array `a`, each with its columns reversed."""

def pick(a, rows, cols):
    """Fancy indexing: the 1-D array of elements a[rows[k], cols[k]].

    `rows` and `cols` are equal-length sequences of indices.
    """
```

Examples:

```python
>>> make_grid(2, 3)
array([[0., 1., 2.],
       [3., 4., 5.]])
>>> checkerboard(3)
array([[0, 1, 0],
       [1, 0, 1],
       [0, 1, 0]])
>>> a = np.arange(12).reshape(3, 4)
>>> every_other_row_reversed(a)
array([[ 3,  2,  1,  0],
       [11, 10,  9,  8]])
>>> pick(a, [0, 2, 1], [3, 0, 2])
array([3, 8, 6])
```
