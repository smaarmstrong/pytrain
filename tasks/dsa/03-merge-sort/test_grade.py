import random
from operator import itemgetter

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return get_attr(mod, "merge"), get_attr(mod, "merge_sort")


def test_merge_basics():
    merge, _ = fns()
    assert merge([1, 4], [2, 3]) == [1, 2, 3, 4]
    assert merge([], []) == []
    assert merge([1, 2], []) == [1, 2]
    assert merge([], [1, 2]) == [1, 2]


def test_merge_ties_prefer_left():
    merge, _ = fns()
    out = merge([(1, "L")], [(1, "R")], key=itemgetter(0))
    assert out == [(1, "L"), (1, "R")]


def test_sort_basics():
    _, ms = fns()
    assert ms([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5]
    assert ms([]) == []
    assert ms([7]) == [7]
    assert ms([2, 2, 2]) == [2, 2, 2]
    assert ms([2, 1]) == [1, 2]


def test_sort_does_not_mutate_input():
    _, ms = fns()
    items = [3, 1, 2]
    out = ms(items)
    assert items == [3, 1, 2]
    assert out is not items


def test_sort_with_key():
    _, ms = fns()
    assert ms(["bb", "a", "ccc"], key=len) == ["a", "bb", "ccc"]


def test_key_only_comparisons():
    # dicts don't support < : only key(x) may be compared.
    _, ms = fns()
    rows = [{"n": 3}, {"n": 1}, {"n": 2}]
    assert ms(rows, key=lambda d: d["n"]) == [{"n": 1}, {"n": 2}, {"n": 3}]


def test_stability_observable():
    _, ms = fns()
    items = [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]
    out = ms(items, key=itemgetter(0))
    assert out == [(1, "b"), (1, "d"), (2, "a"), (2, "c"), (2, "e")]


def test_randomized_against_sorted_oracle():
    _, ms = fns()
    rng = random.Random(42)
    for _ in range(150):
        n = rng.randrange(0, 60)
        # few distinct keys -> lots of ties, so stability differences show up
        items = [(rng.randrange(5), i) for i in range(n)]
        key = itemgetter(0)
        assert ms(items, key=key) == sorted(items, key=key)  # sorted() is stable
        plain = [rng.randrange(100) for _ in range(n)]
        assert ms(plain) == sorted(plain)
