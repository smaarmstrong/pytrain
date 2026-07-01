import random

from pytrain_grader import load_solution, get_attr, time_limited


def k_smallest():
    return get_attr(load_solution(), "k_smallest")


def test_basic():
    f = k_smallest()
    assert f([5, 3, 9, 1, 4], 3) == [1, 3, 4]


def test_returns_a_list_ascending():
    f = k_smallest()
    out = f([7, 2, 8, 2, 5], 4)
    assert isinstance(out, list)
    assert out == sorted(out) == [2, 2, 5, 7]


def test_duplicates_kept():
    f = k_smallest()
    assert f([2, 1, 2, 1], 3) == [1, 1, 2]


def test_k_zero_and_empty():
    f = k_smallest()
    assert f([1, 2, 3], 0) == []
    assert f([], 5) == []


def test_k_exceeds_length():
    f = k_smallest()
    assert f([3, 1, 2], 10) == [1, 2, 3]


def test_one_shot_generator_single_pass():
    f = k_smallest()
    assert f(iter(range(1000, 0, -1)), 2) == [1, 2]


def test_large_input_within_budget():
    f = k_smallest()
    rng = random.Random(42)
    data = [rng.randrange(10**9) for _ in range(500_000)]
    expected = sorted(data)[:10]
    got = time_limited(f, iter(data), 10, seconds=5.0)
    assert got == expected
