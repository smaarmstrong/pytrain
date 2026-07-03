import hashlib

import pytest

from pytrain_grader import load_solution, get_attr


def test_rectangle_area_computed():
    Rectangle = get_attr(load_solution(), "Rectangle")
    assert Rectangle(3, 4).area == 12
    assert Rectangle(width=2, height=5).area == 10
    r = Rectangle(2.5, 4)
    assert r.area == pytest.approx(10.0)


def test_rectangle_area_is_not_a_constructor_arg():
    Rectangle = get_attr(load_solution(), "Rectangle")
    with pytest.raises(TypeError):
        Rectangle(3, 4, 99)


def test_rectangle_validates_dimensions():
    Rectangle = get_attr(load_solution(), "Rectangle")
    with pytest.raises(ValueError):
        Rectangle(0, 5)
    with pytest.raises(ValueError):
        Rectangle(5, -1)


def test_user_stores_hash_not_password():
    User = get_attr(load_solution(), "User")
    u = User("ada", "s3cret")
    assert u.name == "ada"
    assert u.password_hash == hashlib.sha256(b"s3cret").hexdigest()
    assert not hasattr(u, "password")


def test_user_keyword_construction():
    User = get_attr(load_solution(), "User")
    u = User(name="bob", password="hunter2")
    assert u.password_hash == hashlib.sha256(b"hunter2").hexdigest()


def test_user_repr_does_not_leak_password():
    User = get_attr(load_solution(), "User")
    u = User("ada", "s3cret")
    assert "s3cret" not in repr(u)


def test_check_accepts_right_password_only():
    mod = load_solution()
    User = get_attr(mod, "User")
    check = get_attr(mod, "check")
    u = User("ada", "s3cret")
    assert check(u, "s3cret") is True
    assert check(u, "guess") is False
    assert check(u, "") is False
