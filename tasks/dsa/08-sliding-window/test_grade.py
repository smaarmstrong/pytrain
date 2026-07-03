import random

import pytest

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "max_window_sum"),
            get_attr(mod, "longest_unique_substring"),
            get_attr(mod, "pair_with_sum_sorted"))


# --- max_window_sum -------------------------------------------------------

def test_window_sum_basics():
    mws, _, _ = fns()
    assert mws([1, -2, 3, 4, -1], 2) == 7
    assert mws([2, 1, 5, 1, 3, 2], 3) == 9
    assert mws([4], 1) == 4
    assert mws([1, 2, 3], 3) == 6


def test_window_sum_all_negative():
    mws, _, _ = fns()
    assert mws([-5, -1, -8], 2) == -6


def test_window_sum_k_too_big_returns_none():
    mws, _, _ = fns()
    assert mws([5], 3) is None
    assert mws([], 1) is None


def test_window_sum_bad_k_raises():
    mws, _, _ = fns()
    with pytest.raises(ValueError):
        mws([1, 2], 0)
    with pytest.raises(ValueError):
        mws([1, 2], -1)


def test_window_sum_randomized():
    mws, _, _ = fns()
    rng = random.Random(42)
    for _ in range(200):
        nums = [rng.randrange(-10, 11) for _ in range(rng.randrange(1, 40))]
        k = rng.randrange(1, len(nums) + 1)
        oracle = max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))
        assert mws(list(nums), k) == oracle


# --- longest_unique_substring ---------------------------------------------

def oracle_longest_unique(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s) + 1):
            if len(set(s[i:j])) == j - i:
                best = max(best, j - i)
    return best


def test_longest_unique_examples():
    _, lus, _ = fns()
    assert lus("abcabcbb") == 3
    assert lus("pwwkew") == 3
    assert lus("") == 0
    assert lus("aaaa") == 1
    assert lus("abcdef") == 6
    assert lus("x") == 1


def test_longest_unique_window_must_restart_correctly():
    _, lus, _ = fns()
    # trips implementations that reset `left` backwards
    assert lus("abba") == 2
    assert lus("tmmzuxt") == 5


def test_longest_unique_randomized():
    _, lus, _ = fns()
    rng = random.Random(42)
    for _ in range(120):
        s = "".join(rng.choice("abcde") for _ in range(rng.randrange(0, 30)))
        assert lus(s) == oracle_longest_unique(s), s


# --- pair_with_sum_sorted ---------------------------------------------------

def test_pair_examples():
    _, _, pws = fns()
    got = pws([1, 2, 4, 7, 11], 9)
    i, j = got
    nums = [1, 2, 4, 7, 11]
    assert 0 <= i < j < 5 and nums[i] + nums[j] == 9
    assert pws([1, 2], 100) is None
    assert pws([], 3) is None
    assert pws([3], 6) is None


def test_pair_duplicates_and_negatives():
    _, _, pws = fns()
    nums = [-4, -1, -1, 2, 5]
    got = pws(nums, -2)
    i, j = got
    assert i < j and nums[i] + nums[j] == -2


def test_pair_randomized_against_oracle():
    _, _, pws = fns()
    rng = random.Random(42)
    for _ in range(200):
        nums = sorted(rng.randrange(-15, 16) for _ in range(rng.randrange(0, 20)))
        target = rng.randrange(-25, 26)
        oracle_has = any(nums[i] + nums[j] == target
                         for i in range(len(nums)) for j in range(i + 1, len(nums)))
        got = pws(list(nums), target)
        if oracle_has:
            assert got is not None, (nums, target)
            i, j = got
            assert 0 <= i < j < len(nums) and nums[i] + nums[j] == target
        else:
            assert got is None, (nums, target)
