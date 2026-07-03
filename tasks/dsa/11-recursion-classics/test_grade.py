import itertools
import random
from collections import Counter

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "permutations_of"),
            get_attr(mod, "subsets_of"),
            get_attr(mod, "flatten"))


# --- permutations_of --------------------------------------------------------

def perm_canon(result):
    """Order-insensitive multiset of the returned orderings."""
    return Counter(tuple(p) for p in result)


def test_permutations_small():
    pf, _, _ = fns()
    assert pf([]) == [[]]
    assert perm_canon(pf([7])) == Counter({(7,): 1})
    assert perm_canon(pf([1, 2])) == Counter({(1, 2): 1, (2, 1): 1})


def test_permutations_three_distinct():
    pf, _, _ = fns()
    got = pf([1, 2, 3])
    assert len(got) == 6
    assert perm_canon(got) == Counter(itertools.permutations([1, 2, 3]))


def test_permutations_repeated_values_positions_distinct():
    pf, _, _ = fns()
    got = pf([1, 1])
    assert len(got) == 2
    assert perm_canon(got) == Counter({(1, 1): 2})


def test_permutations_does_not_mutate():
    pf, _, _ = fns()
    items = [3, 1, 2]
    pf(items)
    assert items == [3, 1, 2]


def test_permutations_randomized_vs_itertools():
    pf, _, _ = fns()
    rng = random.Random(42)
    for _ in range(20):
        n = rng.randrange(0, 6)
        items = [rng.randrange(4) for _ in range(n)]
        got = pf(list(items))
        assert perm_canon(got) == Counter(itertools.permutations(items)), items


# --- subsets_of -------------------------------------------------------------

def subset_canon(result):
    return sorted(tuple(s) for s in result)


def oracle_subsets(items):
    out = []
    for r in range(len(items) + 1):
        out.extend(itertools.combinations(items, r))
    return sorted(out)


def test_subsets_small():
    _, sf, _ = fns()
    assert sf([]) == [[]]
    assert subset_canon(sf([5])) == [(), (5,)]
    assert subset_canon(sf([1, 2])) == [(), (1,), (1, 2), (2,)]


def test_subsets_count_and_order_within():
    _, sf, _ = fns()
    got = sf([1, 2, 3])
    assert len(got) == 8
    assert subset_canon(got) == oracle_subsets([1, 2, 3])
    # relative order kept: [3, 1] must never appear
    assert all(list(s) == sorted(s, key=[1, 2, 3].index) for s in got)


def test_subsets_randomized():
    _, sf, _ = fns()
    rng = random.Random(42)
    for _ in range(20):
        n = rng.randrange(0, 9)
        items = rng.sample(range(100), n)  # distinct, unsorted
        got = sf(list(items))
        assert len(got) == 2 ** n
        assert subset_canon(got) == oracle_subsets(items), items


# --- flatten ----------------------------------------------------------------

def oracle_flatten(nested):
    out = []
    stack = [iter(nested)]
    while stack:
        try:
            x = next(stack[-1])
        except StopIteration:
            stack.pop()
            continue
        if isinstance(x, list):
            stack.append(iter(x))
        else:
            out.append(x)
    return out


def test_flatten_examples():
    _, _, fl = fns()
    assert fl([1, [2, [3, [4]]], 5]) == [1, 2, 3, 4, 5]
    assert fl([]) == []
    assert fl([[], [[]]]) == []
    assert fl([1, 2, 3]) == [1, 2, 3]


def test_flatten_atoms_not_iterated():
    _, _, fl = fns()
    assert fl(["ab", [1, ("x",)], []]) == ["ab", 1, ("x",)]
    assert fl([None, [None]]) == [None, None]


def test_flatten_deep_nesting():
    _, _, fl = fns()
    nested = [0]
    for i in range(1, 150):
        nested = [i, nested]
    got = fl(nested)
    assert got == list(range(149, -1, -1))


def test_flatten_does_not_mutate():
    _, _, fl = fns()
    nested = [1, [2, [3]]]
    fl(nested)
    assert nested == [1, [2, [3]]]


def test_flatten_randomized():
    _, _, fl = fns()
    rng = random.Random(42)

    def make(depth):
        if depth == 0 or rng.random() < 0.4:
            return rng.randrange(10)
        return [make(depth - 1) for _ in range(rng.randrange(0, 4))]

    for _ in range(80):
        nested = [make(5) for _ in range(rng.randrange(0, 6))]
        assert fl(nested) == oracle_flatten(nested), nested
