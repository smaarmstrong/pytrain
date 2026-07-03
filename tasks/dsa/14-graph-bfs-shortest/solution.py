from collections import deque


def distances_from(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in graph.get(node, ()):
            if nb not in dist:
                dist[nb] = dist[node] + 1
                queue.append(nb)
    return dist


def shortest_path(graph, start, goal):
    if start == goal:
        return [start]
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in graph.get(node, ()):
            if nb in parent:
                continue
            parent[nb] = node
            if nb == goal:
                path = [nb]
                while parent[path[-1]] is not None:
                    path.append(parent[path[-1]])
                return path[::-1]
            queue.append(nb)
    return None
