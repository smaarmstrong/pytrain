import numpy as np


def solve_system(A, b):
    return np.linalg.solve(A, b)


def row_norms(m):
    return np.linalg.norm(m, axis=1)


def nearest(points, target):
    return int(np.argmin(np.linalg.norm(points - target, axis=1)))
