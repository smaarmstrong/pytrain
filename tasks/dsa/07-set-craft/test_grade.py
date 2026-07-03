import random

import pytest

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "dedupe"),
            get_attr(mod, "common_elements"),
            get_attr(mod, "first_unique_window"))


# --- dedupe ---------------------------------------------------------------

def test_dedupe_keeps_first_occurrence_order():
    dd, _, _ = fns()
    assert dd([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert dd(["b", "a", "b"]) == ["b", "a"]


def test_dedupe_edges():
    dd, _, _ = fns()
    assert dd([]) == []
    assert dd([1]) == [1]
    assert dd([5, 5, 5, 5]) == [5]
    original = [2, 2, 1]
    assert dd(original) == [2, 1]
    assert original == [2, 2, 1]  # input untouched


# --- common_elements ------------------------------------------------------

def test_common_elements_basic():
    _, ce, _ = fns()
    assert ce([4, 2, 2, 1], [2, 4, 4, 9]) == [2, 4]
    assert ce([1, 2, 3], [4, 5]) == []


def test_common_elements_edges():
    _, ce, _ = fns()
    assert ce([], [1, 2]) == []
    assert ce([1, 2], []) == []
    assert ce([7, 7], [7, 7, 7]) == [7]
    assert ce([3, 1, 2], [3, 1, 2]) == [1, 2, 3]  # sorted output


def test_common_elements_randomized():
    _, ce, _ = fns()
    rng = random.Random(42)
    for _ in range(100):
        a = [rng.randrange(20) for _ in range(rng.randrange(0, 30))]
        b = [rng.randrange(20) for _ in range(rng.randrange(0, 30))]
        assert ce(a, b) == sorted(set(a) & set(b))


# --- first_unique_window --------------------------------------------------

def oracle_window(items, k):
    for i in range(len(items) - k + 1):
        w = items[i:i + k]
        if len(set(w)) == k:
            return i
    return -1


def test_window_examples():
    _, _, fw = fns()
    assert fw([1, 2, 2, 3, 4, 5], 3) == 2
    assert fw([1, 1, 1], 2) == -1
    assert fw([7], 1) == 0
    assert fw([1, 2, 3], 3) == 0


def test_window_k_bigger_than_input():
    _, _, fw = fns()
    assert fw([1, 2], 3) == -1
    assert fw([], 1) == -1


def test_window_invalid_k_raises():
    _, _, fw = fns()
    with pytest.raises(ValueError):
        fw([1, 2, 3], 0)
    with pytest.raises(ValueError):
        fw([1, 2, 3], -2)


def test_window_match_only_at_the_end():
    _, _, fw = fns()
    assert fw([1, 1, 2, 2, 3, 4], 3) == 3  # [2, 3, 4]


def test_window_randomized_against_oracle():
    _, _, fw = fns()
    rng = random.Random(42)
    for _ in range(200):
        items = [rng.randrange(6) for _ in range(rng.randrange(0, 40))]
        k = rng.randrange(1, 8)
        assert fw(list(items), k) == oracle_window(items, k), (items, k)
