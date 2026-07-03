import bisect
import random

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "binary_search"),
            get_attr(mod, "insert_position"),
            get_attr(mod, "search_rotated"))


def test_binary_search_basics():
    bs, _, _ = fns()
    assert bs([1, 3, 5, 7], 5) == 2
    assert bs([1, 3, 5, 7], 1) == 0
    assert bs([1, 3, 5, 7], 7) == 3
    assert bs([1, 3, 5, 7], 4) == -1
    assert bs([], 1) == -1
    assert bs([9], 9) == 0
    assert bs([9], 8) == -1


def test_binary_search_duplicates_any_matching_index():
    bs, _, _ = fns()
    items = [1, 2, 2, 2, 3]
    idx = bs(items, 2)
    assert idx in (1, 2, 3) and items[idx] == 2


def test_binary_search_randomized():
    bs, _, _ = fns()
    rng = random.Random(42)
    for _ in range(200):
        items = sorted(rng.randrange(50) for _ in range(rng.randrange(0, 30)))
        target = rng.randrange(-5, 55)
        got = bs(items, target)
        if target in items:
            assert 0 <= got < len(items) and items[got] == target
        else:
            assert got == -1


def test_insert_position_basics():
    _, ip, _ = fns()
    assert ip([], 42) == 0
    assert ip([1, 3, 3, 5], 3) == 1     # leftmost, not rightmost
    assert ip([1, 3, 3, 5], 0) == 0
    assert ip([1, 3, 3, 5], 9) == 4
    assert ip([5, 5, 5], 5) == 0


def test_insert_position_matches_bisect_left():
    _, ip, _ = fns()
    rng = random.Random(42)
    for _ in range(300):
        items = sorted(rng.randrange(30) for _ in range(rng.randrange(0, 25)))
        target = rng.randrange(-3, 33)
        assert ip(items, target) == bisect.bisect_left(items, target)


def test_rotated_every_rotation_every_element():
    _, _, sr = fns()
    base = [0, 1, 2, 4, 5, 6, 7]
    for r in range(len(base)):
        nums = base[r:] + base[:r]
        for i, v in enumerate(nums):
            assert sr(nums, v) == i, f"rotation {r}, value {v}"
        assert sr(nums, 3) == -1
        assert sr(nums, -1) == -1
        assert sr(nums, 99) == -1


def test_rotated_edges():
    _, _, sr = fns()
    assert sr([], 5) == -1
    assert sr([5], 5) == 0
    assert sr([5], 4) == -1
    assert sr([2, 1], 1) == 1
    assert sr([2, 1], 2) == 0


def test_rotated_randomized():
    _, _, sr = fns()
    rng = random.Random(42)
    for _ in range(200):
        n = rng.randrange(1, 40)
        base = sorted(rng.sample(range(1000), n))
        r = rng.randrange(n)
        nums = base[r:] + base[:r]
        v = rng.choice(nums)
        assert sr(nums, v) == nums.index(v)
        missing = 1001
        assert sr(nums, missing) == -1
