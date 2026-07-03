# NumPy: axes and masks

In `solution.py` (with `import numpy as np`), implement four functions.
Getting the `axis=` argument right is the whole point of the first two;
boolean masks are the point of the last two. No Python loops.

```python
def row_means(m):
    """1-D array: the mean of each ROW of 2-D array m (length = number of rows)."""

def col_range(m):
    """1-D array: max minus min of each COLUMN of m (length = number of columns)."""

def replace_negatives(a, value):
    """A COPY of array a with every negative element replaced by `value`.

    The input array must NOT be modified.
    """

def rows_where(m, threshold):
    """The rows of 2-D array m whose row-sum is strictly greater than
    `threshold`, as a 2-D array (possibly empty), original row order kept.
    """
```

Examples:

```python
>>> m = np.array([[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]])
>>> row_means(m)
array([ 2., 20.])
>>> col_range(m)
array([ 9., 18., 27.])
>>> replace_negatives(np.array([1, -2, 3, -4]), 0)
array([1, 0, 3, 0])
>>> rows_where(m, 10.0)
array([[10., 20., 30.]])
```
