import numpy as np


def affine(x, scale, shift):
    return x * scale + shift


def standardise(m):
    return (m - m.mean(axis=0)) / m.std(axis=0)


def pairwise_diff(a, b):
    return np.asarray(a)[:, None] - np.asarray(b)[None, :]
