from pytrain_grader import load_solution, get_attr


def test_running_total_accumulates():
    f = get_attr(load_solution(), "running_total")
    assert f([1, 2, 3]) == [1, 3, 6]
    assert f([10, -4, 4]) == [10, 6, 10]


def test_running_total_edges():
    f = get_attr(load_solution(), "running_total")
    assert f([]) == []
    assert f([5]) == [5]


def test_count_vowels_counts_vowels_not_consonants():
    f = get_attr(load_solution(), "count_vowels")
    assert f("debug") == 2
    assert f("aeiou") == 5
    assert f("rhythm") == 0


def test_count_vowels_edges():
    f = get_attr(load_solution(), "count_vowels")
    assert f("") == 0
    assert f("a") == 1
