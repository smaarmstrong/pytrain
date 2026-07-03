# NumPy: solve and norms

In `solution.py` (with `import numpy as np`), implement three functions
around `np.linalg`. Do **not** invert matrices to solve systems
(`np.linalg.solve`, not `inv(A) @ b`), and no Python loops.

```python
def solve_system(A, b):
    """The solution vector x of the linear system A @ x == b.

    A is a square, well-conditioned 2-D array; b is a 1-D array.
    """

def row_norms(m):
    """1-D array of the Euclidean (L2) norm of each ROW of 2-D array m."""

def nearest(points, target):
    """The integer INDEX of the row of `points` (2-D, one point per row)
    closest to the 1-D vector `target` in Euclidean distance.

    Broadcasting + row_norms-style thinking; ties won't occur in the tests.
    """
```

Examples:

```python
>>> solve_system(np.array([[3.0, 1.0], [1.0, 2.0]]), np.array([9.0, 8.0]))
array([2., 3.])
>>> row_norms(np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 1.0]]))
array([5.        , 0.        , 1.41421356])
>>> nearest(np.array([[0.0, 0.0], [5.0, 5.0], [2.0, 2.0]]), np.array([2.1, 1.9]))
2
```
