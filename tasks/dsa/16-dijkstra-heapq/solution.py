import heapq


def dijkstra(graph, start):
    dist = {}
    heap = [(0, id(start), start)]  # id() tie-break keeps nodes un-compared
    while heap:
        d, _, node = heapq.heappop(heap)
        if node in dist:
            continue  # lazy deletion: stale entry
        dist[node] = d
        for nb, w in graph.get(node, ()):
            if nb not in dist:
                heapq.heappush(heap, (d + w, id(nb), nb))
    return dist


def cheapest_route(graph, start, goal):
    dist = {}
    best = {start: 0}   # cheapest tentative cost seen so far
    parent = {start: None}
    heap = [(0, id(start), start)]
    while heap:
        d, _, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        if node == goal:
            path = [node]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return d, path[::-1]
        for nb, w in graph.get(node, ()):
            nd = d + w
            if nb not in dist and (nb not in best or nd < best[nb]):
                best[nb] = nd
                parent[nb] = node
                heapq.heappush(heap, (nd, id(nb), nb))
    return None
