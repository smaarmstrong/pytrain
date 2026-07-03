import itertools
import random

import pytest

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return get_attr(mod, "climb_stairs"), get_attr(mod, "house_robber")


def oracle_stairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def oracle_robber(loot):
    """Brute force over every non-adjacent subset (for small inputs)."""
    n = len(loot)
    best = 0
    for mask in range(1 << n):
        if mask & (mask << 1):
            continue  # adjacent pair chosen
        best = max(best, sum(loot[i] for i in range(n) if mask >> i & 1))
    return best


# --- climb_stairs --------------------------------------------------------------

def test_stairs_base_cases():
    cs, _ = fns()
    assert cs(0) == 1
    assert cs(1) == 1
    assert cs(2) == 2
    assert cs(3) == 3
    assert cs(4) == 5
    assert cs(10) == 89


def test_stairs_negative_raises():
    cs, _ = fns()
    with pytest.raises(ValueError):
        cs(-1)
    with pytest.raises(ValueError):
        cs(-100)


def test_stairs_exact_at_35():
    cs, _ = fns()
    assert cs(35) == 14930352


def test_stairs_n_300_exact():
    # exponential recursion would never finish; any DP answers instantly
    cs, _ = fns()
    assert cs(300) == oracle_stairs(300)
    assert cs(300) == 359579325206583560961765665172189099052367214309267232255589801


def test_stairs_recurrence_holds():
    cs, _ = fns()
    values = [cs(n) for n in range(60)]
    for n in range(2, 60):
        assert values[n] == values[n - 1] + values[n - 2]


# --- house_robber ---------------------------------------------------------------

def test_robber_examples():
    _, hr = fns()
    assert hr([2, 7, 9, 3, 1]) == 12
    assert hr([1, 2, 3, 1]) == 4
    assert hr([2, 1, 1, 2]) == 4


def test_robber_edges():
    _, hr = fns()
    assert hr([]) == 0
    assert hr([5]) == 5
    assert hr([0]) == 0
    assert hr([3, 9]) == 9
    assert hr([0, 0, 0]) == 0


def test_robber_alternating_pattern():
    _, hr = fns()
    assert hr([10, 1, 10, 1, 10]) == 30
    assert hr([1, 10, 1, 10, 1]) == 20


def test_robber_randomized_vs_bruteforce():
    _, hr = fns()
    rng = random.Random(42)
    for _ in range(120):
        loot = [rng.randrange(0, 30) for _ in range(rng.randrange(0, 15))]
        assert hr(list(loot)) == oracle_robber(loot), loot


def test_robber_long_street():
    _, hr = fns()
    rng = random.Random(42)
    loot = [rng.randrange(0, 100) for _ in range(3000)]
    take, skip = 0, 0
    for x in loot:
        take, skip = skip + x, max(take, skip)
    assert hr(list(loot)) == max(take, skip)


def test_robber_exhaustive_length_6():
    _, hr = fns()
    for loot in itertools.product([0, 1, 5], repeat=6):
        assert hr(list(loot)) == oracle_robber(list(loot)), loot
