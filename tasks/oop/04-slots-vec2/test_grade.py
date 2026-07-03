import pytest

from pytrain_grader import load_solution, get_attr


def vec2_cls():
    return get_attr(load_solution(), "Vec2")


def test_construct_and_read():
    Vec2 = vec2_cls()
    v = Vec2(1, 2)
    assert v.x == 1 and v.y == 2


def test_declared_attributes_stay_writable():
    Vec2 = vec2_cls()
    v = Vec2(1, 2)
    v.x = 10
    v.y = -3
    assert v.x == 10 and v.y == -3


def test_undeclared_attribute_raises_attributeerror():
    Vec2 = vec2_cls()
    v = Vec2(1, 2)
    with pytest.raises(AttributeError):
        v.z = 1
    with pytest.raises(AttributeError):
        v.colour = "red"


def test_no_instance_dict():
    Vec2 = vec2_cls()
    assert not hasattr(Vec2(1, 2), "__dict__")


def test_value_equality():
    Vec2 = vec2_cls()
    assert Vec2(1, 2) == Vec2(1, 2)
    assert Vec2(1, 2) != Vec2(1, 3)
    assert Vec2(1, 2) != Vec2(0, 2)


def test_equality_with_other_types_is_false_not_an_error():
    Vec2 = vec2_cls()
    assert (Vec2(1, 2) == (1, 2)) is False
    assert (Vec2(1, 2) == "Vec2(1, 2)") is False


def test_repr_exact():
    Vec2 = vec2_cls()
    assert repr(Vec2(1, 2)) == "Vec2(1, 2)"
    assert repr(Vec2(-1, 2.5)) == "Vec2(-1, 2.5)"


def test_translated_returns_new_and_leaves_original():
    Vec2 = vec2_cls()
    v = Vec2(1, 2)
    w = v.translated(3, -1)
    assert w == Vec2(4, 1)
    assert v == Vec2(1, 2)
    assert w is not v
