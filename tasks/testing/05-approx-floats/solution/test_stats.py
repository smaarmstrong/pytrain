import pytest
from pytest import approx

from stats import mean, normalize, variance


def test_mean_simple():
    assert mean([1.0, 2.0, 3.0, 4.0]) == approx(2.5)


def test_mean_float_noise():
    assert mean([0.1, 0.1, 0.1]) == approx(0.1)


def test_mean_empty_raises():
    with pytest.raises(ValueError):
        mean([])


def test_variance_is_population_variance():
    assert variance([0.1, 0.2, 0.3, 0.4]) == approx(0.0125)


def test_variance_single_value_is_zero():
    assert variance([3.0]) == approx(0.0)


def test_variance_empty_raises():
    with pytest.raises(ValueError):
        variance([])


def test_normalize_matches_expected_collection():
    out = normalize([1.0, 2.0, 3.0])
    assert out == approx([1 / 6, 1 / 3, 1 / 2])
    assert sum(out) == approx(1.0)


def test_normalize_zero_sum_raises_valueerror():
    with pytest.raises(ValueError):
        normalize([1.5, -1.5])
