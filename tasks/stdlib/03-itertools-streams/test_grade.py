import itertools

from pytrain_grader import load_solution, get_attr


def test_take_basic():
    f = get_attr(load_solution(), "take")
    assert f([1, 2, 3, 4], 2) == [1, 2]


def test_take_infinite_iterable():
    f = get_attr(load_solution(), "take")
    assert f(itertools.count(10), 3) == [10, 11, 12]


def test_take_short_and_zero():
    f = get_attr(load_solution(), "take")
    assert f([1, 2], 5) == [1, 2]
    assert f(itertools.count(), 0) == []


def test_flatten():
    f = get_attr(load_solution(), "flatten")
    assert f([[1, 2], (), iter([3])]) == [1, 2, 3]
    assert f([]) == []
    assert f(iter([iter("ab"), iter("c")])) == ["a", "b", "c"]


def test_runs_basic():
    f = get_attr(load_solution(), "runs")
    assert f([1, 1, 2, 2, 2, 3]) == [(1, 2), (2, 3), (3, 1)]


def test_runs_string_and_separated_repeats():
    f = get_attr(load_solution(), "runs")
    assert f("aaabbc") == [("a", 3), ("b", 2), ("c", 1)]
    # non-adjacent equal values are separate runs
    assert f("aba") == [("a", 1), ("b", 1), ("a", 1)]


def test_runs_edges():
    f = get_attr(load_solution(), "runs")
    assert f([]) == []
    assert f([7]) == [(7, 1)]
    assert f(iter([5, 5])) == [(5, 2)]  # one-shot iterable


def test_deltas():
    f = get_attr(load_solution(), "deltas")
    assert f([3, 7, 2]) == [4, -5]
    assert f([5]) == []
    assert f([]) == []
    assert f(iter([1, 4, 9, 16])) == [3, 5, 7]
