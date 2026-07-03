import pytest

from pytrain_grader import load_solution, get_attr


def temperature_cls():
    return get_attr(load_solution(), "Temperature")


def test_constructor_stores_celsius_as_float():
    T = temperature_cls()
    t = T(21)
    assert t.celsius == pytest.approx(21.0)
    assert isinstance(t.celsius, float)


def test_constructor_rejects_below_absolute_zero():
    T = temperature_cls()
    with pytest.raises(ValueError):
        T(-300)
    assert T(-273.15).celsius == pytest.approx(-273.15)  # boundary is valid


def test_from_fahrenheit():
    T = temperature_cls()
    assert T.from_fahrenheit(32).celsius == pytest.approx(0.0)
    assert T.from_fahrenheit(212).celsius == pytest.approx(100.0)
    assert T.from_fahrenheit(-40).celsius == pytest.approx(-40.0)


def test_from_string_celsius():
    T = temperature_cls()
    assert T.from_string("21.5C").celsius == pytest.approx(21.5)
    assert T.from_string("-40c").celsius == pytest.approx(-40.0)


def test_from_string_fahrenheit_converts():
    T = temperature_cls()
    assert T.from_string("212F").celsius == pytest.approx(100.0)
    assert T.from_string("70.7f").celsius == pytest.approx(21.5)


def test_from_string_rejects_garbage():
    T = temperature_cls()
    for bad in ("21.5K", "abcC", "", "C", "12"):
        with pytest.raises(ValueError):
            T.from_string(bad)


def test_is_valid_without_an_instance():
    T = temperature_cls()
    assert T.is_valid(0) is True
    assert T.is_valid(-273.15) is True
    assert T.is_valid(-273.16) is False


def test_classmethods_respect_subclasses():
    T = temperature_cls()

    class Freezer(T):
        pass

    assert isinstance(Freezer.from_fahrenheit(32), Freezer)
    assert isinstance(Freezer.from_string("1C"), Freezer)
