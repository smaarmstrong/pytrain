import numpy as np

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def test_solve_small_system():
    A = np.array([[3.0, 1.0], [1.0, 2.0]])
    b = np.array([9.0, 8.0])
    x = _f("solve_system")(A, b)
    assert np.allclose(x, [2.0, 3.0])


def test_solve_satisfies_system():
    rng = np.random.default_rng(42)
    A = rng.random((5, 5)) + 5.0 * np.eye(5)  # well-conditioned
    b = rng.random(5)
    x = _f("solve_system")(A, b)
    assert np.allclose(A @ np.asarray(x), b)


def test_solve_identity():
    b = np.array([7.0, -1.0, 2.5])
    x = _f("solve_system")(np.eye(3), b)
    assert np.allclose(x, b)


def test_row_norms():
    m = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 1.0]])
    out = _f("row_norms")(m)
    assert np.asarray(out).shape == (3,)
    assert np.allclose(out, [5.0, 0.0, np.sqrt(2.0)])


def test_row_norms_not_col_norms():
    m = np.array([[1.0, 2.0, 2.0], [4.0, 4.0, 2.0]])  # rows -> [3, 6]
    out = _f("row_norms")(m)
    assert np.asarray(out).shape == (2,)
    assert np.allclose(out, [3.0, 6.0])


def test_nearest():
    points = np.array([[0.0, 0.0], [5.0, 5.0], [2.0, 2.0]])
    idx = _f("nearest")(points, np.array([2.1, 1.9]))
    assert int(idx) == 2


def test_nearest_first_point():
    points = np.array([[1.0, 1.0, 1.0], [10.0, 10.0, 10.0]])
    assert int(_f("nearest")(points, np.array([0.9, 1.2, 1.0]))) == 0


def test_nearest_random_cloud():
    rng = np.random.default_rng(42)
    points = rng.random((40, 3))
    target = rng.random(3)
    idx = int(_f("nearest")(points, target))
    dists = np.sqrt(((points - target) ** 2).sum(axis=1))
    assert idx == int(np.argmin(dists))
