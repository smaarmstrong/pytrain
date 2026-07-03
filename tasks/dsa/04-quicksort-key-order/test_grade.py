import random

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return get_attr(mod, "quicksort"), get_attr(mod, "sort_words")


def test_quicksort_basics():
    qs, _ = fns()
    assert qs([3, 1, 2, 1]) == [1, 1, 2, 3]
    assert qs([]) == []
    assert qs([5]) == [5]
    assert qs([2, 2, 2, 2]) == [2, 2, 2, 2]


def test_quicksort_sorted_and_reversed_inputs():
    qs, _ = fns()
    assert qs(list(range(1000))) == list(range(1000))
    assert qs(list(range(1000, 0, -1))) == list(range(1, 1001))


def test_quicksort_does_not_mutate():
    qs, _ = fns()
    items = [3, 1, 2]
    out = qs(items)
    assert items == [3, 1, 2]
    assert out is not items


def test_quicksort_randomized():
    qs, _ = fns()
    rng = random.Random(42)
    for _ in range(100):
        items = [rng.randrange(50) for _ in range(rng.randrange(0, 200))]
        assert qs(items) == sorted(items)


def test_sort_words_length_then_alpha():
    _, sw = fns()
    assert sw(["pear", "Fig", "apple", "fig"]) == ["Fig", "fig", "pear", "apple"]
    assert sw(["b", "A", "ab"]) == ["A", "b", "ab"]
    assert sw([]) == []
    assert sw(["one"]) == ["one"]


def test_sort_words_case_insensitive_tiebreak():
    _, sw = fns()
    assert sw(["banana", "Apple"]) == ["Apple", "banana"]
    assert sw(["b", "A"]) == ["A", "b"]


def test_sort_words_stable_on_full_ties():
    _, sw = fns()
    # same length, same casefolded text -> original order preserved
    assert sw(["AB", "ab", "Ab"]) == ["AB", "ab", "Ab"]
    assert sw(["x", "X", "x"]) == ["x", "X", "x"]


def test_sort_words_does_not_mutate():
    _, sw = fns()
    words = ["bb", "a"]
    out = sw(words)
    assert words == ["bb", "a"]
    assert out == ["a", "bb"]


def test_sort_words_randomized_against_oracle():
    _, sw = fns()
    rng = random.Random(42)
    pool = ["a", "A", "ab", "AB", "Ba", "ba", "abc", "b", "B", "cab", "CaB"]
    for _ in range(100):
        words = [rng.choice(pool) for _ in range(rng.randrange(0, 30))]
        expected = sorted(words, key=lambda w: (len(w), w.casefold()))
        assert sw(list(words)) == expected
