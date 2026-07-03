import operator

from pytrain_grader import load_solution, get_attr


def test_dice_sums_two_d6():
    f = get_attr(load_solution(), "dice_sums")
    d = f(2, 6)
    assert d == {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}


def test_dice_sums_one_die_and_total_count():
    f = get_attr(load_solution(), "dice_sums")
    assert f(1, 4) == {1: 1, 2: 1, 3: 1, 4: 1}
    assert sum(f(3, 6).values()) == 216


def test_unique_anagrams_dedupes():
    f = get_attr(load_solution(), "unique_anagrams")
    assert f("aab") == ["aab", "aba", "baa"]


def test_unique_anagrams_all_distinct_letters():
    f = get_attr(load_solution(), "unique_anagrams")
    assert f("abc") == ["abc", "acb", "bac", "bca", "cab", "cba"]
    assert f("x") == ["x"]
    assert f("aaa") == ["aaa"]


def test_choose_order_and_contents():
    f = get_attr(load_solution(), "choose")
    assert f(["a", "b", "c"], 2) == [("a", "b"), ("a", "c"), ("b", "c")]
    assert f([1, 2, 3, 4], 3) == [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]


def test_choose_edges():
    f = get_attr(load_solution(), "choose")
    assert f(["a", "b"], 0) == [()]
    assert f(["a", "b"], 3) == []


def test_running_add():
    f = get_attr(load_solution(), "running")
    assert f([1, 2, 3, 4], operator.add) == [1, 3, 6, 10]


def test_running_custom_ops_and_edges():
    f = get_attr(load_solution(), "running")
    assert f([3, 1, 4, 1, 5], max) == [3, 3, 4, 4, 5]
    assert f([2, 3, 4], operator.mul) == [2, 6, 24]
    assert f([], operator.add) == []
    assert f([7], operator.add) == [7]
