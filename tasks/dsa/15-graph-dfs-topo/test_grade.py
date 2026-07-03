import random

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "dfs_preorder"),
            get_attr(mod, "has_cycle"),
            get_attr(mod, "topo_sort"))


def node_set(graph):
    nodes = set(graph)
    for nbs in graph.values():
        nodes.update(nbs)
    return nodes


def oracle_dfs(graph, start):
    order, seen = [], set()
    stack = [start]
    # iterative DFS producing the recursive preorder
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        order.append(n)
        stack.extend(reversed(graph.get(n, ())))
    return order


def oracle_has_cycle(graph):
    # Kahn: cyclic iff some node never reaches indegree 0
    nodes = node_set(graph)
    indeg = {n: 0 for n in nodes}
    for nbs in graph.values():
        for v in nbs:
            indeg[v] += 1
    ready = [n for n in nodes if indeg[n] == 0]
    done = 0
    while ready:
        n = ready.pop()
        done += 1
        for v in graph.get(n, ()):
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return done != len(nodes)


def check_topo(graph, order):
    nodes = node_set(graph)
    assert isinstance(order, list)
    assert len(order) == len(nodes) and set(order) == nodes, "must list every node once"
    pos = {n: i for i, n in enumerate(order)}
    for u, nbs in graph.items():
        for v in nbs:
            assert pos[u] < pos[v], f"edge {u}->{v} violated"


def random_dag(rng, n, p=0.2):
    """Random DAG: edges only go 'forward' along a shuffled ranking."""
    nodes = list(range(n))
    rng.shuffle(nodes)
    graph = {u: [] for u in nodes}
    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            if rng.random() < p:
                graph[u].append(v)
    return graph


# --- dfs_preorder ---------------------------------------------------------------

def test_dfs_examples():
    dfs, _, _ = fns()
    assert dfs({"a": ["b", "c"], "b": ["c"]}, "a") == ["a", "b", "c"]
    assert dfs({"a": ["c", "b"], "b": [], "c": []}, "a") == ["a", "c", "b"]


def test_dfs_goes_deep_before_wide():
    dfs, _, _ = fns()
    g = {1: [2, 5], 2: [3], 3: [4], 4: [], 5: [6], 6: []}
    assert dfs(g, 1) == [1, 2, 3, 4, 5, 6]


def test_dfs_never_revisits_on_cycles():
    dfs, _, _ = fns()
    g = {"a": ["b"], "b": ["c"], "c": ["a", "b"]}
    assert dfs(g, "a") == ["a", "b", "c"]
    g2 = {"x": ["x", "y"], "y": []}  # self-loop
    assert dfs(g2, "x") == ["x", "y"]


def test_dfs_start_only_reaches_its_component():
    dfs, _, _ = fns()
    g = {"a": ["b"], "b": [], "z": ["q"], "q": []}
    assert dfs(g, "a") == ["a", "b"]
    assert dfs(g, "lonely") == ["lonely"]  # start with no key


def test_dfs_randomized_exact_order():
    dfs, _, _ = fns()
    rng = random.Random(42)
    for _ in range(50):
        n = rng.randrange(1, 20)
        graph = {u: rng.sample(range(n), rng.randrange(0, n)) for u in range(n)}
        start = rng.randrange(n)
        assert dfs(graph, start) == oracle_dfs(graph, start), (graph, start)


# --- has_cycle -------------------------------------------------------------------

def test_cycle_basics():
    _, hc, _ = fns()
    assert hc({}) is False
    assert hc({"a": []}) is False
    assert hc({"a": ["b"], "b": ["a"]}) is True
    assert hc({"a": ["a"]}) is True  # self-loop


def test_diamond_is_not_a_cycle():
    _, hc, _ = fns()
    assert hc({"a": ["b", "c"], "b": ["d"], "c": ["d"]}) is False


def test_cycle_not_reachable_from_first_key():
    _, hc, _ = fns()
    # cycle sits in a separate component; every node must be considered
    g = {"a": ["b"], "b": [], "p": ["q"], "q": ["p"]}
    assert hc(g) is True


def test_long_chain_then_back_edge():
    _, hc, _ = fns()
    chain = {i: [i + 1] for i in range(50)}
    chain[50] = []
    assert hc(chain) is False
    chain[50] = [17]
    assert hc(chain) is True


def test_cycle_randomized():
    _, hc, _ = fns()
    rng = random.Random(42)
    for _ in range(60):
        n = rng.randrange(1, 18)
        graph = {u: rng.sample(range(n), rng.randrange(0, min(n, 4))) for u in range(n)}
        assert hc(graph) is oracle_has_cycle(graph), graph


# --- topo_sort --------------------------------------------------------------------

def test_topo_examples():
    _, _, ts = fns()
    assert ts({}) == []
    assert ts({"cook": ["eat"], "shop": ["cook"], "eat": []}) == ["shop", "cook", "eat"]
    assert ts({"a": ["b"], "b": ["a"]}) is None
    assert ts({"a": ["a"]}) is None


def test_topo_includes_neighbour_only_nodes():
    _, _, ts = fns()
    g = {"a": ["b", "c"]}  # b, c have no keys of their own
    check_topo(g, ts(g))


def test_topo_disconnected():
    _, _, ts = fns()
    g = {1: [2], 3: [4], 5: []}
    check_topo(g, ts(g))


def test_topo_any_valid_order_accepted():
    _, _, ts = fns()
    g = {"a": ["c"], "b": ["c"], "c": ["d"], "d": []}
    check_topo(g, ts(g))


def test_topo_randomized_dags_and_cyclic_graphs():
    _, _, ts = fns()
    rng = random.Random(42)
    for _ in range(50):
        n = rng.randrange(1, 20)
        graph = random_dag(rng, n)
        check_topo(graph, ts(graph))
        # sabotage: add a back edge to force a cycle
        order = oracle_dfs(graph, next(iter(graph)))
        if len(order) >= 2:
            u, v = order[-1], order[0]
            cyclic = {k: list(vs) for k, vs in graph.items()}
            cyclic.setdefault(u, [])
            if v not in cyclic[u]:
                cyclic[u] = cyclic[u] + [v]
            if oracle_has_cycle(cyclic):
                assert ts(cyclic) is None, cyclic
