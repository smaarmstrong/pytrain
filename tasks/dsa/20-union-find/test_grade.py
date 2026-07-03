import random

import pytest

from pytrain_grader import load_solution, get_attr


def api():
    mod = load_solution()
    return get_attr(mod, "DisjointSet"), get_attr(mod, "count_components")


class OracleDSU:
    """Trivially-correct sets-of-frozensets bookkeeping."""

    def __init__(self):
        self.groups = {}  # element -> set of elements (shared object)

    def add(self, x):
        if x not in self.groups:
            self.groups[x] = {x}

    def union(self, a, b):
        self.add(a)
        self.add(b)
        ga, gb = self.groups[a], self.groups[b]
        if ga is gb:
            return False
        ga |= gb
        for x in gb:
            self.groups[x] = ga
        return True

    def connected(self, a, b):
        return a in self.groups and b in self.groups and self.groups[a] is self.groups[b]


# --- basic behaviour ---------------------------------------------------------

def test_singletons_after_add():
    DS, _ = api()
    ds = DS()
    ds.add("a")
    ds.add("b")
    assert ds.find("a") == "a"          # a singleton's representative is itself
    assert ds.connected("a", "a") is True
    assert ds.connected("a", "b") is False


def test_add_is_idempotent():
    DS, _ = api()
    ds = DS()
    ds.add(1)
    ds.add(2)
    ds.union(1, 2)
    ds.add(1)  # must NOT reset 1 into its own group
    assert ds.connected(1, 2) is True


def test_find_unknown_raises_keyerror():
    DS, _ = api()
    ds = DS()
    ds.add("known")
    with pytest.raises(KeyError):
        ds.find("unknown")


def test_connected_unknown_is_false():
    DS, _ = api()
    ds = DS()
    ds.add("a")
    assert ds.connected("a", "ghost") is False
    assert ds.connected("ghost", "a") is False
    assert ds.connected("ghost", "ghost") is False


def test_union_return_values():
    DS, _ = api()
    ds = DS()
    assert ds.union("a", "b") is True    # auto-adds both
    assert ds.union("b", "a") is False   # already together
    assert ds.union("a", "a") is False   # same element
    assert ds.union("b", "c") is True
    assert ds.union("c", "a") is False   # transitively together already


def test_transitive_connectivity():
    DS, _ = api()
    ds = DS()
    ds.union(1, 2)
    ds.union(3, 4)
    assert ds.connected(1, 3) is False
    ds.union(2, 3)
    for a in (1, 2, 3, 4):
        for b in (1, 2, 3, 4):
            assert ds.connected(a, b) is True
    assert ds.connected(1, 5) is False


def test_find_consistent_within_a_group():
    DS, _ = api()
    ds = DS()
    for x in "abcdef":
        ds.add(x)
    ds.union("a", "b")
    ds.union("c", "d")
    ds.union("b", "c")
    reps = {ds.find(x) for x in "abcd"}
    assert len(reps) == 1, "one merged group must have one representative"
    rep = reps.pop()
    assert rep in set("abcd"), "representative must belong to the group"
    assert ds.find("e") != rep and ds.find("f") != rep


def test_mixed_hashable_elements():
    DS, _ = api()
    ds = DS()
    ds.union(("tup", 1), "string")
    ds.add(42)
    assert ds.connected(("tup", 1), "string") is True
    assert ds.connected(42, "string") is False


# --- randomized cross-check ---------------------------------------------------

def test_randomized_against_oracle():
    DS, _ = api()
    rng = random.Random(42)
    ds, oracle = DS(), OracleDSU()
    elements = list(range(300))
    for step in range(4000):
        op = rng.random()
        a, b = rng.choice(elements), rng.choice(elements)
        if op < 0.15:
            ds.add(a)
            oracle.add(a)
        elif op < 0.55:
            known_a, known_b = a in oracle.groups, b in oracle.groups
            got = ds.union(a, b)
            assert got is oracle.union(a, b), (step, a, b, known_a, known_b)
        else:
            assert ds.connected(a, b) is oracle.connected(a, b), (step, a, b)
    # final full agreement, including find() self-consistency
    known = list(oracle.groups)
    for a in known:
        assert ds.find(a) in oracle.groups[a], "representative outside its group"
    for _ in range(2000):
        a, b = rng.choice(known), rng.choice(known)
        same = oracle.connected(a, b)
        assert ds.connected(a, b) is same
        assert (ds.find(a) == ds.find(b)) is same


# --- count_components -----------------------------------------------------------

def test_components_examples():
    _, cc = api()
    assert cc(5, [(0, 1), (1, 2)]) == 3
    assert cc(4, [(0, 1), (2, 3)]) == 2
    assert cc(4, []) == 4
    assert cc(0, []) == 0
    assert cc(1, []) == 1


def test_components_duplicates_and_self_loops():
    _, cc = api()
    assert cc(3, [(0, 1), (1, 0), (0, 1), (2, 2)]) == 2
    assert cc(2, [(0, 0), (1, 1)]) == 2


def test_components_everything_linked():
    _, cc = api()
    assert cc(6, [(i, i + 1) for i in range(5)]) == 1
    assert cc(6, [(0, i) for i in range(1, 6)]) == 1  # star shape


def test_components_randomized_vs_bfs_oracle():
    _, cc = api()
    rng = random.Random(42)
    for _ in range(60):
        n = rng.randrange(0, 40)
        edges = [(rng.randrange(n), rng.randrange(n))
                 for _ in range(rng.randrange(0, 50))] if n else []
        adj = {u: set() for u in range(n)}
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        seen, comps = set(), 0
        for s in range(n):
            if s in seen:
                continue
            comps += 1
            stack = [s]
            while stack:
                u = stack.pop()
                if u in seen:
                    continue
                seen.add(u)
                stack.extend(adj[u] - seen)
        assert cc(n, list(edges)) == comps, (n, edges)


def test_components_large_promptly():
    _, cc = api()
    rng = random.Random(42)
    n = 5000
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(8000)]
    got = cc(n, edges)
    # independent oracle count
    oracle = OracleDSU()
    for x in range(n):
        oracle.add(x)
    merges = sum(oracle.union(u, v) for u, v in edges)
    assert got == n - merges
