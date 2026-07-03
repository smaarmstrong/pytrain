import random
from collections import deque

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return get_attr(mod, "distances_from"), get_attr(mod, "shortest_path")


def oracle_distances(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in graph.get(node, ()):
            if nb not in dist:
                dist[nb] = dist[node] + 1
                queue.append(nb)
    return dist


def edges_of(graph):
    return {(u, v) for u, nbs in graph.items() for v in nbs}


def check_path(graph, start, goal, path):
    """path must be a valid start->goal walk over real edges."""
    assert isinstance(path, list)
    assert path[0] == start and path[-1] == goal
    es = edges_of(graph)
    for u, v in zip(path, path[1:]):
        assert (u, v) in es, f"{u}->{v} is not an edge"


G = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}


# --- distances_from -----------------------------------------------------------

def test_distances_example():
    df, _ = fns()
    assert df(G, "a") == {"a": 0, "b": 1, "c": 1, "d": 2}


def test_distances_unreachable_excluded():
    df, _ = fns()
    g = {"a": ["b"], "b": [], "x": ["y"], "y": []}
    assert df(g, "a") == {"a": 0, "b": 1}


def test_distances_start_without_key():
    df, _ = fns()
    assert df({"a": ["b"]}, "z") == {"z": 0}
    assert df({}, "z") == {"z": 0}


def test_distances_cycle_and_self_loop():
    df, _ = fns()
    g = {"a": ["a", "b"], "b": ["c"], "c": ["a"]}
    assert df(g, "a") == {"a": 0, "b": 1, "c": 2}


def test_distances_duplicate_neighbours():
    df, _ = fns()
    g = {"a": ["b", "b", "b"], "b": []}
    assert df(g, "a") == {"a": 0, "b": 1}


def test_distances_shortcut_wins():
    df, _ = fns()
    # long way round exists, but the direct edge decides the distance
    g = {"s": ["m", "t"], "m": ["t"], "t": []}
    assert df(g, "s")["t"] == 1


# --- shortest_path --------------------------------------------------------------

def test_path_example_and_validity():
    _, sp = fns()
    path = sp(G, "a", "d")
    check_path(G, "a", "d", path)
    assert len(path) == 3  # exactly the BFS-shortest length


def test_path_start_equals_goal():
    _, sp = fns()
    assert sp(G, "a", "a") == ["a"]
    assert sp({}, "x", "x") == ["x"]


def test_path_none_when_unreachable():
    _, sp = fns()
    assert sp(G, "d", "a") is None
    assert sp(G, "a", "zebra") is None       # goal not in graph at all
    assert sp({"a": []}, "a", "b") is None


def test_path_through_cycles():
    _, sp = fns()
    g = {1: [2], 2: [3, 1], 3: [1, 4], 4: []}
    path = sp(g, 1, 4)
    check_path(g, 1, 4, path)
    assert len(path) == 4  # 1-2-3-4


def test_randomized_against_bfs_oracle():
    df, sp = fns()
    rng = random.Random(42)
    for _ in range(60):
        n = rng.randrange(1, 25)
        nodes = list(range(n))
        graph = {u: [v for v in nodes
                     if v != u and rng.random() < 0.12] for u in nodes}
        start = rng.choice(nodes)
        assert df(graph, start) == oracle_distances(graph, start)
        goal = rng.choice(nodes)
        oracle = oracle_distances(graph, start)
        path = sp(graph, start, goal)
        if goal not in oracle:
            assert path is None, (graph, start, goal)
        elif start == goal:
            assert path == [start]
        else:
            check_path(graph, start, goal, path)
            assert len(path) == oracle[goal] + 1, (graph, start, goal, path)
