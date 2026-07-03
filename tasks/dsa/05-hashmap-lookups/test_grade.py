import random
from collections import Counter

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "char_frequency"),
            get_attr(mod, "two_sum"),
            get_attr(mod, "group_anagrams"))


# --- char_frequency -------------------------------------------------------

def test_char_frequency_basic():
    cf, _, _ = fns()
    assert dict(cf("aab")) == {"a": 2, "b": 1}
    assert dict(cf("")) == {}
    assert dict(cf("z")) == {"z": 1}


def test_char_frequency_case_and_punctuation():
    cf, _, _ = fns()
    assert dict(cf("Aa a!")) == {"A": 1, "a": 2, " ": 1, "!": 1}


def test_char_frequency_randomized():
    cf, _, _ = fns()
    rng = random.Random(42)
    for _ in range(50):
        s = "".join(rng.choice("abcXYZ 12!") for _ in range(rng.randrange(0, 80)))
        assert dict(cf(s)) == dict(Counter(s))


# --- two_sum --------------------------------------------------------------

def check_pair(nums, target, got):
    """got must be a valid (i, j) pair."""
    assert got is not None, f"expected a pair for nums={nums}, target={target}"
    i, j = got
    assert 0 <= i < j < len(nums), f"bad indices {got}"
    assert nums[i] + nums[j] == target


def test_two_sum_basic():
    _, ts, _ = fns()
    check_pair([2, 7, 11, 15], 9, ts([2, 7, 11, 15], 9))
    check_pair([3, 2, 4], 6, ts([3, 2, 4], 6))


def test_two_sum_same_value_twice_needs_two_indices():
    _, ts, _ = fns()
    check_pair([3, 3], 6, ts([3, 3], 6))
    assert ts([3], 6) is None  # an element can't pair with itself


def test_two_sum_no_pair_and_empty():
    _, ts, _ = fns()
    assert ts([], 5) is None
    assert ts([1, 2, 3], 100) is None


def test_two_sum_negatives_and_zero_target():
    _, ts, _ = fns()
    check_pair([-3, 1, 3], 0, ts([-3, 1, 3], 0))
    check_pair([-5, -7, -2], -12, ts([-5, -7, -2], -12))


def test_two_sum_randomized_against_oracle():
    _, ts, _ = fns()
    rng = random.Random(42)
    for _ in range(200):
        nums = [rng.randrange(-20, 21) for _ in range(rng.randrange(0, 25))]
        target = rng.randrange(-30, 31)
        oracle_has = any(nums[i] + nums[j] == target
                         for i in range(len(nums)) for j in range(i + 1, len(nums)))
        got = ts(list(nums), target)
        if oracle_has:
            check_pair(nums, target, got)
        else:
            assert got is None


# --- group_anagrams -------------------------------------------------------

def canon(groups):
    """Order-insensitive canonical form (handles duplicate words)."""
    return sorted(tuple(sorted(g)) for g in groups)


def test_group_anagrams_classic():
    _, _, ga = fns()
    out = ga(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert canon(out) == canon([["eat", "tea", "ate"], ["tan", "nat"], ["bat"]])


def test_group_anagrams_edges():
    _, _, ga = fns()
    assert ga([]) == []
    assert canon(ga(["solo"])) == [("solo",)]
    # case-sensitive: "Ab" is not an anagram of "ab"
    assert canon(ga(["Ab", "ab", "ba"])) == canon([["Ab"], ["ab", "ba"]])


def test_group_anagrams_duplicates_kept():
    _, _, ga = fns()
    out = ga(["aa", "aa", "ab"])
    assert canon(out) == canon([["aa", "aa"], ["ab"]])
    assert sum(len(g) for g in out) == 3


def test_group_anagrams_randomized():
    _, _, ga = fns()
    rng = random.Random(42)
    pool = ["abc", "bca", "cab", "abd", "dab", "xy", "yx", "z", ""]
    for _ in range(60):
        words = [rng.choice(pool) for _ in range(rng.randrange(0, 20))]
        expected = {}
        for w in words:
            expected.setdefault("".join(sorted(w)), []).append(w)
        assert canon(ga(list(words))) == canon(expected.values())
