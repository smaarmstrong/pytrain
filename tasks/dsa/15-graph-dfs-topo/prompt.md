# Graphs: DFS, cycles, topological sort

Directed graphs again arrive as adjacency dicts `{node: [neighbour, ...]}`.
A node mentioned only as a neighbour (no key of its own) has no outgoing
edges. **The node set of the graph = all keys plus all mentioned
neighbours.** Neighbour lists contain no duplicates.

In `solution.py`, implement:

```python
def dfs_preorder(graph, start):
    """Depth-first visit order starting at `start`, as a list.

    Visit a node, then explore its neighbours IN LIST ORDER, fully
    exploring each branch before the next (classic DFS). Never revisit a
    node. This order is deterministic and the grader checks it exactly.

    dfs_preorder({"a": ["b", "c"], "b": ["c"]}, "a") == ["a", "b", "c"]
    (from "b" we go deep to "c" before returning to try "a"'s "c").
    """

def has_cycle(graph):
    """True iff ANY directed cycle exists anywhere in the graph.

    Consider every node, not just some start; a self-loop is a cycle.
    A node revisited via two DIFFERENT branches (a diamond a->b, a->c,
    b->d, c->d) is NOT a cycle — you need a directed loop.
    """

def topo_sort(graph):
    """A topological order of ALL nodes of the graph, as a list.

    Every node appears exactly once, and for every edge u -> v, u comes
    somewhere before v. If the graph contains a cycle, return None.
    Any valid order is accepted. {} -> [].
    """
```

Requirements:

- `dfs_preorder`: recursion or an explicit stack both work — but with a
  stack, take care to still produce the recursive (list-order) sequence.
- `has_cycle` must distinguish "currently on the recursion path" from
  "finished earlier" (the diamond case above), e.g. the three-colour
  scheme or Kahn's algorithm.
- Graphs may be disconnected; `topo_sort` still lists every node.

Examples:

```python
>>> g = {"cook": ["eat"], "shop": ["cook"], "eat": []}
>>> topo_sort(g)
['shop', 'cook', 'eat']
>>> has_cycle({"a": ["b"], "b": ["a"]})
True
>>> has_cycle({"a": ["b", "c"], "b": ["d"], "c": ["d"]})
False
>>> topo_sort({"a": ["b"], "b": ["a"]}) is None
True
```
