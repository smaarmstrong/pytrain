import pytest

from pytrain_grader import load_solution, get_attr


def api():
    mod = load_solution()
    return (get_attr(mod, "Checkout"), get_attr(mod, "no_discount"),
            get_attr(mod, "percent_off"), get_attr(mod, "bulk_discount"))


def test_default_strategy_is_no_discount():
    Checkout, *_ = api()
    assert Checkout().total([1.0, 2.0]) == pytest.approx(3.0)


def test_no_discount_returns_zero():
    _, no_discount, *_ = api()
    assert no_discount(123.45) == 0


def test_percent_off():
    Checkout, _, percent_off, _ = api()
    assert Checkout(percent_off(10)).total([6.0, 4.0]) == pytest.approx(9.0)
    assert Checkout(percent_off(50)).total([10.0]) == pytest.approx(5.0)


def test_bulk_discount_threshold_semantics():
    Checkout, _, _, bulk_discount = api()
    c = Checkout(bulk_discount(50, 20))
    assert c.total([30.0]) == pytest.approx(30.0)   # under threshold
    assert c.total([60.0]) == pytest.approx(48.0)   # over
    assert c.total([50.0]) == pytest.approx(40.0)   # boundary counts


def test_any_callable_works_as_a_strategy():
    Checkout, *_ = api()
    assert Checkout(lambda s: 5).total([12.0]) == pytest.approx(7.0)
    assert Checkout(lambda s: s / 2).total([8.0]) == pytest.approx(4.0)


def test_swapping_strategy_changes_behaviour():
    Checkout, _, percent_off, _ = api()
    c = Checkout()
    assert c.total([10.0]) == pytest.approx(10.0)
    c.strategy = percent_off(50)
    assert c.total([10.0]) == pytest.approx(5.0)
    c.strategy = lambda s: 1
    assert c.total([10.0]) == pytest.approx(9.0)


def test_total_never_negative():
    Checkout, *_ = api()
    assert Checkout(lambda s: 999).total([10.0]) == pytest.approx(0.0)


def test_empty_prices():
    Checkout, *_ = api()
    assert Checkout().total([]) == pytest.approx(0.0)


def test_rounding_to_two_decimals():
    Checkout, _, percent_off, _ = api()
    assert Checkout(percent_off(15)).total([9.99]) == pytest.approx(8.49)
