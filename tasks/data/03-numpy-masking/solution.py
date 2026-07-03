import numpy as np


def row_means(m):
    return m.mean(axis=1)


def col_range(m):
    return m.max(axis=0) - m.min(axis=0)


def replace_negatives(a, value):
    out = np.array(a, copy=True)
    out[out < 0] = value
    return out


def rows_where(m, threshold):
    return m[m.sum(axis=1) > threshold]
