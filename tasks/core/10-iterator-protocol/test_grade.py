import pytest

from pytrain_grader import load_solution, get_attr


def countdown_cls():
    return get_attr(load_solution(), "Countdown")


def test_basic_sequence():
    C = countdown_cls()
    assert list(C(3)) == [3, 2, 1]
    assert list(C(1)) == [1]


def test_empty_for_zero_and_negative():
    C = countdown_cls()
    assert list(C(0)) == []
    assert list(C(-5)) == []


def test_reiterable_not_one_shot():
    C = countdown_cls()
    c = C(3)
    assert list(c) == [3, 2, 1]
    assert list(c) == [3, 2, 1], "Countdown must be an iterable, not a one-shot iterator"


def test_independent_iterators():
    C = countdown_cls()
    c = C(3)
    it1, it2 = iter(c), iter(c)
    assert next(it1) == 3
    assert next(it1) == 2
    assert next(it2) == 3  # it2 unaffected by it1's progress
    assert next(it1) == 1
    assert next(it2) == 2


def test_manual_next_and_stopiteration():
    C = countdown_cls()
    it = iter(C(2))
    assert next(it) == 2
    assert next(it) == 1
    with pytest.raises(StopIteration):
        next(it)
    with pytest.raises(StopIteration):
        next(it)  # stays exhausted, never restarts


def test_iterator_is_its_own_iterator():
    C = countdown_cls()
    it = iter(C(3))
    assert iter(it) is it
    next(it)
    # a half-consumed iterator resumes where it left off in a for loop
    rest = [x for x in it]
    assert rest == [2, 1]


def test_works_in_for_loop_and_unpacking():
    C = countdown_cls()
    out = []
    for x in C(4):
        out.append(x)
    assert out == [4, 3, 2, 1]
    a, b, c = C(3)
    assert (a, b, c) == (3, 2, 1)
