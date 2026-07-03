import pytest

from pytrain_grader import load_solution, get_attr


def product_cls():
    return get_attr(load_solution(), "Product")


def test_constructor_and_getter():
    Product = product_cls()
    p = Product("tea", 2.5)
    assert p.name == "tea"
    assert p.price == pytest.approx(2.5)


def test_int_price_comes_back_as_float():
    Product = product_cls()
    p = Product("tea", 3)
    assert p.price == pytest.approx(3.0)
    assert isinstance(p.price, float)


def test_default_price_is_zero():
    Product = product_cls()
    assert Product("free").price == pytest.approx(0.0)


def test_setter_rejects_negative_and_keeps_old_value():
    Product = product_cls()
    p = Product("tea", 2.5)
    with pytest.raises(ValueError):
        p.price = -0.01
    assert p.price == pytest.approx(2.5)


def test_constructor_validates_through_the_property():
    Product = product_cls()
    with pytest.raises(ValueError):
        Product("bad", -5)


def test_deleter_resets_to_zero_and_stays_usable():
    Product = product_cls()
    p = Product("tea", 2.5)
    del p.price
    assert p.price == pytest.approx(0.0)
    p.price = 3.0
    assert p.price == pytest.approx(3.0)


def test_currency_is_shared_via_the_class():
    Product = product_cls()
    a = Product("a", 1)
    b = Product("b", 2)
    assert a.currency == "GBP" and b.currency == "GBP"
    Product.currency = "EUR"
    assert a.currency == "EUR" and b.currency == "EUR"


def test_instance_currency_shadows_only_that_instance():
    Product = product_cls()
    a = Product("a", 1)
    b = Product("b", 2)
    b.currency = "USD"
    assert b.currency == "USD"
    assert a.currency == "GBP"
