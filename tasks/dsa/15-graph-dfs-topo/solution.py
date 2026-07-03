def all_nodes(graph):
    nodes = list(graph)
    seen = set(graph)
    for nbs in graph.values():
        for v in nbs:
            if v not in seen:
                seen.add(v)
                nodes.append(v)
    return nodes


def dfs_preorder(graph, start):
    order, seen = [], set()

    def visit(node):
        if node in seen:
            return
        seen.add(node)
        order.append(node)
        for nb in graph.get(node, ()):
            visit(nb)

    visit(start)
    return order


def has_cycle(graph):
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {}

    def visit(node):
        colour[node] = GREY
        for nb in graph.get(node, ()):
            c = colour.get(nb, WHITE)
            if c == GREY:
                return True
            if c == WHITE and visit(nb):
                return True
        colour[node] = BLACK
        return False

    for node in all_nodes(graph):
        if colour.get(node, WHITE) == WHITE and visit(node):
            return True
    return False


def topo_sort(graph):
    nodes = all_nodes(graph)
    indeg = {n: 0 for n in nodes}
    for nbs in graph.values():
        for v in nbs:
            indeg[v] += 1
    ready = [n for n in nodes if indeg[n] == 0]
    order = []
    while ready:
        n = ready.pop()
        order.append(n)
        for v in graph.get(n, ()):
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return order if len(order) == len(nodes) else None
