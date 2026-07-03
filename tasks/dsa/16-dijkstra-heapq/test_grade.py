import random

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return get_attr(mod, "dijkstra"), get_attr(mod, "cheapest_route")


def oracle_costs(graph, start):
    """Bellman-Ford: trivially correct, no heap subtleties."""
    nodes = set(graph) | {v for nbs in graph.values() for v, _ in nbs} | {start}
    INF = float("inf")
    dist = {n: INF for n in nodes}
    dist[start] = 0
    for _ in range(len(nodes)):
        changed = False
        for u, nbs in graph.items():
            if dist[u] == INF:
                continue
            for v, w in nbs:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    changed = True
        if not changed:
            break
    return {n: d for n, d in dist.items() if d != INF}


def min_edge_cost(graph, u, v):
    ws = [w for nb, w in graph.get(u, ()) if nb == v]
    assert ws, f"{u}->{v} is not an edge"
    return min(ws)


def check_route(graph, start, goal, expected_cost, got):
    assert got is not None, f"expected a route {start}->{goal}"
    cost, path = got
    assert cost == expected_cost
    assert isinstance(path, list)
    assert path[0] == start and path[-1] == goal
    walked = sum(min_edge_cost(graph, u, v) for u, v in zip(path, path[1:]))
    assert walked == cost, f"path {path} costs {walked}, claimed {cost}"


G = {"s": [("a", 1), ("b", 5)], "a": [("b", 1)], "b": [("t", 1)]}


# --- dijkstra ------------------------------------------------------------------

def test_costs_example():
    dj, _ = fns()
    assert dj(G, "s") == {"s": 0, "a": 1, "b": 2, "t": 3}


def test_costs_cheap_beats_few_hops():
    dj, _ = fns()
    g = {"s": [("t", 10), ("a", 1)], "a": [("b", 1)], "b": [("t", 1)]}
    assert dj(g, "s")["t"] == 3  # 3 hops beat the direct edge


def test_costs_unreachable_excluded_and_lonely_start():
    dj, _ = fns()
    g = {"a": [("b", 2)], "x": [("y", 1)]}
    assert dj(g, "a") == {"a": 0, "b": 2}
    assert dj({}, "z") == {"z": 0}


def test_costs_zero_weight_and_self_loop():
    dj, _ = fns()
    g = {"a": [("a", 0), ("b", 0)], "b": [("c", 7)]}
    assert dj(g, "a") == {"a": 0, "b": 0, "c": 7}


def test_costs_parallel_edges_take_cheapest():
    dj, _ = fns()
    g = {"a": [("b", 9), ("b", 2), ("b", 5)]}
    assert dj(g, "a") == {"a": 0, "b": 2}


def test_costs_cycle_does_not_loop_forever():
    dj, _ = fns()
    g = {1: [(2, 1)], 2: [(3, 1)], 3: [(1, 1)]}
    assert dj(g, 1) == {1: 0, 2: 1, 3: 2}


def test_costs_randomized_vs_bellman_ford():
    dj, _ = fns()
    rng = random.Random(42)
    for _ in range(50):
        n = rng.randrange(1, 15)
        graph = {u: [(rng.randrange(n), rng.randrange(0, 10))
                     for _ in range(rng.randrange(0, 5))] for u in range(n)}
        start = rng.randrange(n)
        assert dj(graph, start) == oracle_costs(graph, start), (graph, start)


# --- cheapest_route --------------------------------------------------------------

def test_route_example():
    _, cr = fns()
    check_route(G, "s", "t", 3, cr(G, "s", "t"))


def test_route_start_equals_goal():
    _, cr = fns()
    assert cr(G, "s", "s") == (0, ["s"])
    assert cr({}, "x", "x") == (0, ["x"])


def test_route_unreachable_is_none():
    _, cr = fns()
    assert cr(G, "t", "s") is None
    assert cr(G, "s", "nowhere") is None
    assert cr({"a": []}, "a", "b") is None


def test_route_prefers_cheap_over_short():
    _, cr = fns()
    g = {"s": [("t", 10), ("a", 1)], "a": [("b", 1)], "b": [("t", 1)]}
    check_route(g, "s", "t", 3, cr(g, "s", "t"))


def test_route_with_zero_weights():
    _, cr = fns()
    g = {"s": [("a", 0)], "a": [("t", 0)]}
    check_route(g, "s", "t", 0, cr(g, "s", "t"))


def test_route_randomized_vs_oracle():
    _, cr = fns()
    rng = random.Random(42)
    for _ in range(60):
        n = rng.randrange(1, 15)
        graph = {u: [(rng.randrange(n), rng.randrange(0, 10))
                     for _ in range(rng.randrange(0, 5))] for u in range(n)}
        start, goal = rng.randrange(n), rng.randrange(n)
        oracle = oracle_costs(graph, start)
        got = cr(graph, start, goal)
        if goal not in oracle:
            assert got is None, (graph, start, goal)
        elif start == goal:
            assert got == (0, [start])
        else:
            check_route(graph, start, goal, oracle[goal], got)
