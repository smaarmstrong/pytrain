import numpy as np


def affine(x, scale, shift):
    """Elementwise x * scale + shift. Vectorised — the grader times this on
    5 million elements with a 2 s budget."""
    raise NotImplementedError


def standardise(m):
    """Z-score each column of m ((m - column mean) / column std, ddof=0)."""
    raise NotImplementedError


def pairwise_diff(a, b):
    """out[i, j] = a[i] - b[j] via broadcasting; shape (len(a), len(b))."""
    raise NotImplementedError
