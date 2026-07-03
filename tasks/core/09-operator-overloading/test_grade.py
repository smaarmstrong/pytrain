import pytest

from pytrain_grader import load_solution, get_attr


def duration_cls():
    return get_attr(load_solution(), "Duration")


def test_add_duration_plus_duration():
    D = duration_cls()
    out = D(60) + D(30)
    assert isinstance(out, D)
    assert out.seconds == 90


def test_add_int_right_operand():
    D = duration_cls()
    out = D(60) + 30
    assert isinstance(out, D) and out.seconds == 90


def test_reflected_add():
    D = duration_cls()
    out = 30 + D(60)
    assert isinstance(out, D) and out.seconds == 90


def test_sum_builtin_works():
    D = duration_cls()
    total = sum([D(1), D(2), D(3)])
    assert isinstance(total, D) and total.seconds == 6


def test_add_incompatible_raises_typeerror():
    D = duration_cls()
    with pytest.raises(TypeError):
        D(1) + "x"
    with pytest.raises(TypeError):
        "x" + D(1)


def test_multiplication_both_sides():
    D = duration_cls()
    assert (D(60) * 3).seconds == 180
    assert (3 * D(60)).seconds == 180
    assert isinstance(2 * D(5), D)
    with pytest.raises(TypeError):
        D(5) * "a"


def test_operands_not_mutated():
    D = duration_cls()
    a, b = D(10), D(20)
    _ = a + b
    _ = a * 2
    assert a.seconds == 10 and b.seconds == 20


def test_equality():
    D = duration_cls()
    assert D(60) == D(60)
    assert D(60) != D(61)
    assert (D(60) == 60) is False  # not equal to plain numbers
    assert (60 == D(60)) is False


def test_ordering():
    D = duration_cls()
    assert D(59) < D(60)
    assert D(60) <= D(60)
    assert D(61) > D(60)
    assert D(60) >= D(60)
    assert not (D(60) < D(60))


def test_sorting():
    D = duration_cls()
    out = sorted([D(3), D(1), D(2)])
    assert [d.seconds for d in out] == [1, 2, 3]


def test_ordering_with_foreign_type_raises():
    D = duration_cls()
    with pytest.raises(TypeError):
        D(1) < "x"
