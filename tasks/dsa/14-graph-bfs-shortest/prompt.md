# Graphs: BFS shortest path

Graphs arrive as an **adjacency dict**: `{node: [neighbour, ...], ...}`.
Edges are DIRECTED (`"a": ["b"]` does not imply an edge b→a; an undirected
graph simply lists both directions). Nodes are hashable (strings/ints).
A node that appears only as someone's neighbour may be missing from the
dict's keys — treat it as having no outgoing edges. Neighbour lists may
contain duplicates and self-loops; neither changes any distance.

In `solution.py`, implement:

```python
def distances_from(graph, start):
    """Return {node: hops} for every node REACHABLE from start via BFS.

    start is always included with distance 0 (even when it has no key in
    `graph`). Unreachable nodes must NOT appear in the result.
    """

def shortest_path(graph, start, goal):
    """Return one SHORTEST path [start, ..., goal] as a list of nodes.

    - Consecutive path entries must be actual edges of `graph`.
    - When several shortest paths exist, ANY one of them is accepted.
    - start == goal -> [start].
    - No path -> None.
    """
```

Requirements:

- Breadth-first search with a queue (`collections.deque`) is the intended
  technique — depth-first walks find *a* path, not a shortest one, and the
  grader checks lengths exactly.
- Handles: cycles, disconnected components, goal absent from the graph
  entirely, self-loops.

Examples:

```python
>>> g = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
>>> distances_from(g, "a")
{'a': 0, 'b': 1, 'c': 1, 'd': 2}
>>> shortest_path(g, "a", "d")     # ['a', 'c', 'd'] equally fine
['a', 'b', 'd']
>>> shortest_path(g, "d", "a") is None
True
>>> shortest_path({}, "x", "x")
['x']
```
