import pytest

from pytrain_grader import load_solution, get_attr


def test_divide_returns_true_division():
    divide = get_attr(load_solution(), "divide")
    assert divide(10, 2) == 5.0
    assert divide(1, 4) == 0.25
    assert divide(-9, 3) == -3.0


def test_divide_lets_zero_division_raise():
    divide = get_attr(load_solution(), "divide")
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_test_divide_passes_against_the_correct_divide():
    mod = load_solution()
    test_fn = get_attr(mod, "test_divide")
    test_fn()  # must complete without raising


def test_test_divide_catches_wrong_answers():
    # A real test must FAIL when divide is broken. Swap in an impl that
    # returns garbage; the learner's test_divide must raise.
    mod = load_solution()
    test_fn = get_attr(mod, "test_divide")
    mod.divide = lambda a, b: 0
    with pytest.raises(BaseException):
        test_fn()


def test_test_divide_checks_the_zero_case():
    # This impl divides correctly but returns 999 instead of raising on
    # b == 0 — only a test that covers ZeroDivisionError will catch it.
    mod = load_solution()
    test_fn = get_attr(mod, "test_divide")
    mod.divide = lambda a, b: a / b if b else 999
    with pytest.raises(BaseException):
        test_fn()
