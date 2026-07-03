import itertools

import pytest

from pytrain_grader import load_solution, get_attr


def tracking_source(values, log):
    """Yield values, recording each one actually pulled."""
    for v in values:
        log.append(v)
        yield v


def test_eager_returns_correct_list():
    f = get_attr(load_solution(), "eager_squares")
    out = f([1, 2, 3])
    assert out == [1, 4, 9]
    assert isinstance(out, list)
    assert f([]) == []


def test_eager_consumes_input_immediately():
    f = get_attr(load_solution(), "eager_squares")
    log = []
    f(tracking_source([1, 2, 3], log))
    assert log == [1, 2, 3], "eager_squares must consume its whole input at call time"


def test_lazy_consumes_nothing_at_call_time():
    f = get_attr(load_solution(), "lazy_squares")
    log = []
    f(tracking_source([1, 2, 3], log))
    assert log == [], "calling lazy_squares must not consume any input yet"


def test_lazy_pulls_one_item_per_next():
    f = get_attr(load_solution(), "lazy_squares")
    log = []
    it = f(tracking_source([2, 3, 4], log))
    assert next(it) == 4
    assert log == [2], f"one next() should pull exactly one input item, pulled {log}"
    assert next(it) == 9
    assert log == [2, 3]


def test_lazy_values_correct_when_fully_consumed():
    f = get_attr(load_solution(), "lazy_squares")
    assert list(f([1, 2, 3])) == [1, 4, 9]
    assert list(f([])) == []


def test_lazy_handles_unbounded_input():
    f = get_attr(load_solution(), "lazy_squares")
    it = f(itertools.count(1))
    assert [next(it) for _ in range(3)] == [1, 4, 9]


def test_lazy_is_one_shot():
    f = get_attr(load_solution(), "lazy_squares")
    g = f([2, 3])
    assert list(g) == [4, 9]
    assert list(g) == []
    with pytest.raises(StopIteration):
        next(g)


def test_lazy_is_not_a_list():
    f = get_attr(load_solution(), "lazy_squares")
    out = f([1])
    assert not isinstance(out, list)
    assert hasattr(out, "__next__"), "lazy_squares must return an iterator"
