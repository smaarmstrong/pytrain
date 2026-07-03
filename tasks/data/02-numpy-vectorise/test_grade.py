import numpy as np

from pytrain_grader import load_solution, get_attr, time_limited


def _f(name):
    return get_attr(load_solution(), name)


def test_affine_small():
    out = _f("affine")(np.array([1.0, 2.0, 3.0]), 2.0, 1.0)
    assert np.allclose(out, [3.0, 5.0, 7.0])


def test_affine_negative_scale():
    out = _f("affine")(np.array([0.0, 4.0]), -0.5, 10.0)
    assert np.allclose(out, [10.0, 8.0])


def test_affine_does_not_mutate_input():
    x = np.array([1.0, 2.0])
    _f("affine")(x, 3.0, 0.0)
    assert np.allclose(x, [1.0, 2.0])


def test_affine_vectorised_within_time_budget():
    rng = np.random.default_rng(42)
    x = rng.random(5_000_000)
    out = time_limited(_f("affine"), x, 2.0, 0.5, seconds=2.0)
    out = np.asarray(out)
    assert out.shape == (5_000_000,)
    assert np.allclose(out[:10], x[:10] * 2.0 + 0.5)
    assert np.allclose(out[-10:], x[-10:] * 2.0 + 0.5)


def test_standardise_columns():
    m = np.array([[1.0, 10.0], [3.0, 30.0]])
    out = _f("standardise")(m)
    assert np.allclose(out, [[-1.0, -1.0], [1.0, 1.0]])


def test_standardise_result_has_zero_mean_unit_std():
    rng = np.random.default_rng(42)
    m = rng.normal(loc=5.0, scale=3.0, size=(50, 4))
    out = _f("standardise")(m)
    assert out.shape == (50, 4)
    assert np.allclose(out.mean(axis=0), 0.0, atol=1e-9)
    assert np.allclose(out.std(axis=0), 1.0, atol=1e-9)


def test_standardise_exact_formula():
    rng = np.random.default_rng(7)
    m = rng.random((10, 3)) * 100
    out = _f("standardise")(m)
    expected = (m - m.mean(axis=0)) / m.std(axis=0)
    assert np.allclose(out, expected)


def test_pairwise_diff():
    a = np.array([1.0, 2.0])
    b = np.array([10.0, 20.0, 30.0])
    out = _f("pairwise_diff")(a, b)
    assert out.shape == (2, 3)
    assert np.allclose(out, [[-9.0, -19.0, -29.0], [-8.0, -18.0, -28.0]])


def test_pairwise_diff_single_elements():
    out = _f("pairwise_diff")(np.array([5.0]), np.array([3.0]))
    assert out.shape == (1, 1)
    assert np.allclose(out, [[2.0]])
