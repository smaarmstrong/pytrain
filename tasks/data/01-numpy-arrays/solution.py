import numpy as np


def make_grid(rows, cols):
    return np.arange(rows * cols, dtype=np.float64).reshape(rows, cols)


def checkerboard(n):
    board = np.zeros((n, n), dtype=np.int64)
    board[::2, 1::2] = 1
    board[1::2, ::2] = 1
    return board


def every_other_row_reversed(a):
    return a[::2, ::-1]


def pick(a, rows, cols):
    return a[np.asarray(rows), np.asarray(cols)]
