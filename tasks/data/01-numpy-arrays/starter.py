import numpy as np


def make_grid(rows, cols):
    """2-D float array (rows, cols) counting 0, 1, 2, ... row by row."""
    raise NotImplementedError


def checkerboard(n):
    """n x n integer array where cell [i, j] == (i + j) % 2."""
    raise NotImplementedError


def every_other_row_reversed(a):
    """Rows 0, 2, 4, ... of `a`, each with columns reversed."""
    raise NotImplementedError


def pick(a, rows, cols):
    """1-D array of elements a[rows[k], cols[k]] via fancy indexing."""
    raise NotImplementedError
