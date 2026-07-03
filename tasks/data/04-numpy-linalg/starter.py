import numpy as np


def solve_system(A, b):
    """Solution x of A @ x == b (use np.linalg.solve, not inv)."""
    raise NotImplementedError


def row_norms(m):
    """L2 norm of each row of m."""
    raise NotImplementedError


def nearest(points, target):
    """Index of the row of points closest to target (Euclidean)."""
    raise NotImplementedError
