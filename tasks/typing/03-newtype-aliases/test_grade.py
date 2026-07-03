import pytest

from pytrain_grader import load_solution, get_attr


def test_userid_is_a_newtype_over_int():
    UserId = get_attr(load_solution(), "UserId")
    assert getattr(UserId, "__supertype__", None) is int, (
        "UserId must be typing.NewType('UserId', int)"
    )
    assert UserId(7) == 7
    assert type(UserId(7)) is int  # NewType is erased at runtime


def test_vector_aliases_list_of_float():
    Vector = get_attr(load_solution(), "Vector")
    # `type Vector = ...` gives a TypeAliasType with __value__; a plain or
    # TypeAlias assignment IS the aliased type. Accept both.
    underlying = getattr(Vector, "__value__", Vector)
    assert underlying == list[float], (
        f"Vector must alias list[float], got {underlying!r}"
    )


def test_make_user_id_validates():
    f = get_attr(load_solution(), "make_user_id")
    assert f(7) == 7
    assert f(1) == 1
    with pytest.raises(ValueError):
        f(0)
    with pytest.raises(ValueError):
        f(-3)


def test_scale_returns_new_list():
    f = get_attr(load_solution(), "scale")
    v = [1.0, 2.5]
    assert f(v, 2.0) == [2.0, 5.0]
    assert v == [1.0, 2.5], "scale must not mutate its input"
    assert f([], 3.0) == []


def test_lookup():
    mod = load_solution()
    UserId = get_attr(mod, "UserId")
    f = get_attr(mod, "lookup")
    names = {UserId(1): "ada", UserId(2): "grace"}
    assert f(names, UserId(2)) == "grace"
    assert f(names, UserId(99)) is None
    assert f({}, UserId(1)) is None
