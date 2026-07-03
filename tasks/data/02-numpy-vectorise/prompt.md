# NumPy: no loops allowed

In `solution.py` (with `import numpy as np`), implement three functions using
**vectorised numpy arithmetic and broadcasting only — no Python-level loops**
(no `for`/`while`, no comprehensions over array elements, no `map`).

The grader enforces this behaviourally: `affine` is run on an array of
5,000,000 elements under a 2-second wall-clock budget. Vectorised code takes
milliseconds; an element-by-element Python loop takes several seconds and
fails.

```python
def affine(x, scale, shift):
    """Elementwise x * scale + shift for a 1-D array x; returns a new array."""

def standardise(m):
    """Z-score each COLUMN of 2-D array m: subtract the column mean, divide
    by the column standard deviation (population std, ddof=0).

    Broadcasting does this in one expression — no loops over columns.
    """

def pairwise_diff(a, b):
    """The (len(a), len(b)) 'outer difference' matrix: out[i, j] = a[i] - b[j].

    Hint: reshape one operand to a column with a[:, None] and let
    broadcasting do the rest.
    """
```

Examples:

```python
>>> affine(np.array([1.0, 2.0, 3.0]), 2.0, 1.0)
array([3., 5., 7.])
>>> standardise(np.array([[1.0, 10.0], [3.0, 30.0]]))
array([[-1., -1.],
       [ 1.,  1.]])
>>> pairwise_diff(np.array([1.0, 2.0]), np.array([10.0, 20.0, 30.0]))
array([[ -9., -19., -29.],
       [ -8., -18., -28.]])
```
