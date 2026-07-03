import random

from pytrain_grader import load_solution, get_attr, time_limited


def fns():
    mod = load_solution()
    return get_attr(mod, "max_subarray_sum"), get_attr(mod, "range_sums")


def oracle_max_subarray(nums):
    return max(sum(nums[i:j]) for i in range(len(nums)) for j in range(i + 1, len(nums) + 1))


def oracle_ranges(nums, queries):
    return [sum(nums[lo:hi]) for lo, hi in queries]


# --- max_subarray_sum: correctness ------------------------------------------

def test_max_subarray_examples():
    ms, _ = fns()
    assert ms([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert ms([5, -9, 6, -2, 3]) == 7
    assert ms([1, 2, 3]) == 6


def test_max_subarray_edges():
    ms, _ = fns()
    assert ms([7]) == 7
    assert ms([-7]) == -7
    assert ms([-8, -3, -6]) == -3       # non-empty: best single element
    assert ms([0, 0, 0]) == 0
    assert ms([-1, 0, -2]) == 0


def test_max_subarray_run_in_the_middle():
    ms, _ = fns()
    assert ms([-10, 5, 5, -10]) == 10
    assert ms([3, -1, 3, -10, 2]) == 5


def test_max_subarray_randomized_vs_bruteforce():
    ms, _ = fns()
    rng = random.Random(42)
    for _ in range(200):
        nums = [rng.randrange(-20, 21) for _ in range(rng.randrange(1, 30))]
        assert ms(list(nums)) == oracle_max_subarray(nums), nums


# --- max_subarray_sum: the O(n) budget ---------------------------------------

def test_max_subarray_large_n_within_budget():
    ms, _ = fns()
    rng = random.Random(42)
    nums = [rng.randrange(-1000, 1001) for _ in range(500_000)]
    # reference (Kadane) runs this in well under a second; budget is ~10x.
    got = time_limited(ms, nums, seconds=8.0)
    # verify against an independent O(n) computation
    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur < 0 else cur + x
        best = max(best, cur)
    assert got == best


# --- range_sums: correctness ---------------------------------------------------

def test_range_sums_examples():
    _, rs = fns()
    assert rs([2, 4, 6, 8], [(0, 4), (1, 3), (2, 2)]) == [20, 10, 0]
    assert rs([5], [(0, 1), (0, 0), (1, 1)]) == [5, 0, 0]


def test_range_sums_edges():
    _, rs = fns()
    assert rs([], [(0, 0)]) == [0]
    assert rs([1, 2], []) == []
    assert rs([-3, 3], [(0, 2)]) == [0]
    # duplicate and unsorted queries answered in the order given
    assert rs([1, 2, 3], [(2, 3), (0, 1), (2, 3)]) == [3, 1, 3]


def test_range_sums_randomized_vs_bruteforce():
    _, rs = fns()
    rng = random.Random(42)
    for _ in range(100):
        n = rng.randrange(0, 40)
        nums = [rng.randrange(-9, 10) for _ in range(n)]
        queries = []
        for _ in range(rng.randrange(0, 15)):
            lo = rng.randrange(0, n + 1)
            hi = rng.randrange(lo, n + 1)
            queries.append((lo, hi))
        assert rs(list(nums), list(queries)) == oracle_ranges(nums, queries), (nums, queries)


# --- range_sums: the O(n + q) budget --------------------------------------------

def test_range_sums_many_wide_queries_within_budget():
    _, rs = fns()
    rng = random.Random(42)
    n = 200_000
    nums = [rng.randrange(-100, 101) for _ in range(n)]
    # wide ranges: naive per-query summing does ~1.5e10 element-adds and
    # cannot finish; prefix sums answer all 100k in a blink.
    queries = [(rng.randrange(0, n // 4), rng.randrange(3 * n // 4, n + 1))
               for _ in range(100_000)]
    got = time_limited(rs, nums, queries, seconds=8.0)
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    expected = [prefix[hi] - prefix[lo] for lo, hi in queries]
    assert got == expected
    # spot-check a few against true brute force too
    for lo, hi in queries[:5]:
        assert sum(nums[lo:hi]) == prefix[hi] - prefix[lo]
