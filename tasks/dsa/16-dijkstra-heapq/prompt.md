# Dijkstra with heapq

Weighted directed graphs arrive as `{node: [(neighbour, weight), ...], ...}`
with integer weights `>= 0` (zero-weight edges are legal). The same
neighbour may appear several times with different weights (parallel edges —
only the cheapest can ever matter). Nodes missing from the keys have no
outgoing edges.

In `solution.py`, implement:

```python
def dijkstra(graph, start):
    """Cheapest-cost table from start: {node: cost} for every REACHABLE
    node. start always included with cost 0. Unreachable nodes absent.

    Use the classic heapq-powered algorithm: pop the cheapest frontier
    node, relax its edges, push improvements. Entries popped after their
    node already has a final cost are simply skipped ("lazy deletion" —
    the same trick 06's k-smallest used for efficiency).
    """

def cheapest_route(graph, start, goal):
    """Return (cost, path) for ONE cheapest start->goal route, where
    `path` is the node list [start, ..., goal].

    - Any cheapest path is accepted; its edge-costs must sum to `cost`.
    - start == goal -> (0, [start]).
    - Unreachable -> None.
    """
```

Requirements:

- Handles: cycles, self-loops, zero-weight edges, parallel edges,
  disconnected nodes, goal absent entirely.
- Costs are exact integers (no float drift).
- Greedy-by-cheapest matters: the grader includes graphs where the path
  with the fewest hops is NOT the cheapest, so BFS gives wrong answers.

Examples:

```python
>>> g = {"s": [("a", 1), ("b", 5)], "a": [("b", 1)], "b": [("t", 1)]}
>>> dijkstra(g, "s")
{'s': 0, 'a': 1, 'b': 2, 't': 3}
>>> cheapest_route(g, "s", "t")
(3, ['s', 'a', 'b', 't'])
>>> cheapest_route(g, "t", "s") is None
True
>>> cheapest_route({}, "x", "x")
(0, ['x'])
```
