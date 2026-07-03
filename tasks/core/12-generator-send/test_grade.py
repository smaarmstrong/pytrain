import itertools

import pytest

from pytrain_grader import load_solution, get_attr


def test_chunks_basic():
    f = get_attr(load_solution(), "chunks")
    assert list(f([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(f([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
    assert list(f("abcde", 3)) == [["a", "b", "c"], ["d", "e"]]


def test_chunks_edges():
    f = get_attr(load_solution(), "chunks")
    assert list(f([], 3)) == []
    assert list(f([7], 5)) == [[7]]
    assert list(f([1, 2], 1)) == [[1], [2]]


def test_chunks_size_below_one_raises():
    f = get_attr(load_solution(), "chunks")
    with pytest.raises(ValueError):
        list(f([1, 2], 0))


def test_chunks_lazy_on_unbounded_input():
    f = get_attr(load_solution(), "chunks")
    g = f(itertools.count(), 3)
    assert next(g) == [0, 1, 2]
    assert next(g) == [3, 4, 5]


def test_chunks_consumption_is_bounded():
    f = get_attr(load_solution(), "chunks")
    log = []

    def source():
        for v in range(100):
            log.append(v)
            yield v

    g = f(source(), 4)
    assert next(g) == [0, 1, 2, 3]
    assert len(log) <= 5, f"first chunk of 4 should consume ~4 items, consumed {len(log)}"


def test_chunks_yields_fresh_lists():
    f = get_attr(load_solution(), "chunks")
    g = f([1, 2, 3, 4], 2)
    first = next(g)
    first.append(99)
    assert next(g) == [3, 4]


def test_averager_running_mean():
    f = get_attr(load_solution(), "averager")
    g = f()
    assert next(g) is None, "the priming next() should yield None"
    assert g.send(10) == 10.0
    assert g.send(20) == 15.0
    assert g.send(4) == pytest.approx(34 / 3)


def test_averager_returns_floats():
    f = get_attr(load_solution(), "averager")
    g = f()
    next(g)
    out = g.send(10)
    assert isinstance(out, float)


def test_averager_instances_independent():
    f = get_attr(load_solution(), "averager")
    a, b = f(), f()
    next(a)
    next(b)
    assert a.send(100) == 100.0
    assert b.send(2) == 2.0
    assert a.send(0) == 50.0  # state kept per generator


def test_averager_state_survives_many_sends():
    f = get_attr(load_solution(), "averager")
    g = f()
    next(g)
    for i in range(1, 11):
        out = g.send(i)
    assert out == pytest.approx(5.5)
