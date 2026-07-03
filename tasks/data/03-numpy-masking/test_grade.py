import numpy as np

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def test_row_means():
    m = np.array([[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]])
    out = _f("row_means")(m)
    assert np.asarray(out).shape == (2,)
    assert np.allclose(out, [2.0, 20.0])


def test_row_means_not_column_means():
    # A non-square matrix catches axis mix-ups by shape alone.
    m = np.array([[1.0, 3.0], [5.0, 7.0], [9.0, 11.0]])
    out = _f("row_means")(m)
    assert np.asarray(out).shape == (3,)
    assert np.allclose(out, [2.0, 6.0, 10.0])


def test_col_range():
    m = np.array([[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]])
    out = _f("col_range")(m)
    assert np.asarray(out).shape == (3,)
    assert np.allclose(out, [9.0, 18.0, 27.0])


def test_col_range_single_row_is_zero():
    m = np.array([[4.0, 5.0]])
    assert np.allclose(_f("col_range")(m), [0.0, 0.0])


def test_replace_negatives():
    a = np.array([1, -2, 3, -4])
    out = _f("replace_negatives")(a, 0)
    assert np.array_equal(np.asarray(out), [1, 0, 3, 0])


def test_replace_negatives_no_negatives():
    a = np.array([1.0, 2.0])
    assert np.allclose(_f("replace_negatives")(a, 99.0), [1.0, 2.0])


def test_replace_negatives_does_not_mutate_input():
    a = np.array([-1.0, 2.0, -3.0])
    _f("replace_negatives")(a, 0.0)
    assert np.allclose(a, [-1.0, 2.0, -3.0])


def test_rows_where():
    m = np.array([[1.0, 1.0], [5.0, 5.0], [2.0, 2.0]])
    out = _f("rows_where")(m, 3.9)
    assert np.allclose(out, [[5.0, 5.0], [2.0, 2.0]])


def test_rows_where_strictly_greater():
    m = np.array([[2.0, 2.0], [3.0, 3.0]])
    out = _f("rows_where")(m, 4.0)  # row 0 sums to exactly 4.0 -> excluded
    assert np.allclose(out, [[3.0, 3.0]])


def test_rows_where_none_match():
    m = np.array([[1.0, 1.0]])
    out = np.asarray(_f("rows_where")(m, 100.0))
    assert out.shape[0] == 0
