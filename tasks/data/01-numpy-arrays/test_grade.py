import numpy as np

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def test_make_grid_values_and_shape():
    g = _f("make_grid")(3, 4)
    assert isinstance(g, np.ndarray)
    assert g.shape == (3, 4)
    assert np.allclose(g, np.arange(12).reshape(3, 4))


def test_make_grid_single_row():
    g = _f("make_grid")(1, 5)
    assert g.shape == (1, 5)
    assert np.allclose(g, [[0, 1, 2, 3, 4]])


def test_make_grid_dtype_is_floating():
    g = _f("make_grid")(2, 2)
    assert np.issubdtype(g.dtype, np.floating)


def test_checkerboard_even():
    b = _f("checkerboard")(4)
    expected = [[(i + j) % 2 for j in range(4)] for i in range(4)]
    assert isinstance(b, np.ndarray)
    assert b.shape == (4, 4)
    assert np.array_equal(b, expected)
    assert np.issubdtype(b.dtype, np.integer)


def test_checkerboard_odd():
    b = _f("checkerboard")(5)
    expected = [[(i + j) % 2 for j in range(5)] for i in range(5)]
    assert np.array_equal(b, expected)


def test_checkerboard_one():
    b = _f("checkerboard")(1)
    assert b.shape == (1, 1)
    assert b[0, 0] == 0


def test_every_other_row_reversed():
    a = np.arange(20).reshape(4, 5)
    out = _f("every_other_row_reversed")(a)
    assert np.array_equal(out, [[4, 3, 2, 1, 0], [14, 13, 12, 11, 10]])


def test_every_other_row_reversed_single_row():
    a = np.array([[7, 8, 9]])
    out = _f("every_other_row_reversed")(a)
    assert np.array_equal(out, [[9, 8, 7]])


def test_pick():
    a = np.arange(12).reshape(3, 4)
    out = _f("pick")(a, [0, 2, 1], [3, 0, 2])
    assert np.array_equal(np.asarray(out), [3, 8, 6])


def test_pick_repeats_allowed():
    a = np.arange(6).reshape(2, 3)
    out = _f("pick")(a, [1, 1, 0], [0, 0, 2])
    assert np.array_equal(np.asarray(out), [3, 3, 2])
