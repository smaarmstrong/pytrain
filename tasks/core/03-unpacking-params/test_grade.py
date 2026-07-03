import pytest

from pytrain_grader import load_solution, get_attr


def test_head_tail_basic():
    f = get_attr(load_solution(), "head_tail")
    assert f([1, 2, 3, 4]) == (1, [2, 3], 4)
    assert f(("x", "y", "z")) == ("x", ["y"], "z")


def test_head_tail_two_items_and_strings():
    f = get_attr(load_solution(), "head_tail")
    assert f("ab") == ("a", [], "b")
    first, middle, last = f([5, 6])
    assert (first, last) == (5, 6)
    assert middle == [] and isinstance(middle, list)


def test_head_tail_too_short_raises():
    f = get_attr(load_solution(), "head_tail")
    with pytest.raises(ValueError):
        f([1])
    with pytest.raises(ValueError):
        f([])


def test_merge_left_to_right_and_overrides():
    f = get_attr(load_solution(), "merge")
    assert f({"a": 1}, {"a": 2, "b": 3}, a=9) == {"a": 9, "b": 3}
    assert f({"x": 1}, {"y": 2}) == {"x": 1, "y": 2}
    assert f() == {}
    assert f(a=1) == {"a": 1}


def test_merge_does_not_mutate_inputs():
    f = get_attr(load_solution(), "merge")
    d1, d2 = {"a": 1}, {"b": 2}
    out = f(d1, d2, c=3)
    assert d1 == {"a": 1} and d2 == {"b": 2}
    assert out == {"a": 1, "b": 2, "c": 3}
    assert out is not d1 and out is not d2


def test_clamp_behaviour():
    f = get_attr(load_solution(), "clamp")
    assert f(15, 0, 10) == 10
    assert f(-3, 0, 10) == 0
    assert f(5, 0, 10) == 5
    assert f(5, lo=0, hi=10) == 5  # lo/hi may be keywords


def test_clamp_value_is_positional_only():
    f = get_attr(load_solution(), "clamp")
    with pytest.raises(TypeError):
        f(value=5, lo=0, hi=10)


def test_clamp_strict_is_keyword_only():
    f = get_attr(load_solution(), "clamp")
    with pytest.raises(TypeError):
        f(5, 0, 10, True)
    assert f(5, 0, 10, strict=True) == 5
    with pytest.raises(ValueError):
        f(15, 0, 10, strict=True)
    with pytest.raises(ValueError):
        f(-1, lo=0, hi=10, strict=True)
