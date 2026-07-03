# Union-find: disjoint sets

A disjoint-set (union-find) structure tracks a collection of elements
partitioned into non-overlapping groups, supporting near-constant-time
"are these two connected?" and "merge these two groups" operations. It's
the backbone of Kruskal's MST, network-connectivity and clustering code.

In `solution.py`, implement:

```python
class DisjointSet:
    """Elements are arbitrary hashable values, added lazily."""

    def add(self, x):
        """Register x as its own singleton group. Adding an element that
        is already present changes nothing."""

    def find(self, x):
        """Return the REPRESENTATIVE of x's group: some element of that
        group, the same one for every member while the partition is
        unchanged (find(a) == find(b) iff a and b share a group).
        Raise KeyError if x was never added."""

    def union(self, a, b):
        """Merge the groups of a and b (auto-`add`ing either if unknown).
        Return True if two DIFFERENT groups were merged, False if a and b
        were already together (or are the same element)."""

    def connected(self, a, b):
        """True iff a and b are both present and share a group.
        Unknown elements are connected to nothing (return False — even
        connected(x, x) is False for an unknown x)."""

def count_components(n, edges):
    """Number of connected groups among the nodes 0..n-1, where each
    (u, v) pair in `edges` links two nodes (undirected).

    n == 0 -> 0. Isolated nodes each count as their own component.
    Duplicate edges and self-loops (u == u) are harmless.
    count_components(5, [(0, 1), (1, 2)]) == 3   # {0,1,2} {3} {4}
    """
```

Requirements:

- Which element ends up as a representative is your choice — the grader
  only ever compares `find` results to each other and to the group's
  membership; it never expects a particular element.
- The classic implementation keeps a parent pointer per element with path
  compression and union by rank/size. The grader runs thousands of mixed
  operations — anything polynomial passes, but this is the structure to
  learn here.
- `count_components` should be built ON a `DisjointSet` (the grader can't
  check that, but it's the point of the exercise).

Examples:

```python
>>> ds = DisjointSet()
>>> ds.union("a", "b")
True
>>> ds.union("b", "a")
False
>>> ds.connected("a", "b"), ds.connected("a", "z")
(True, False)
>>> count_components(4, [(0, 1), (2, 3)])
2
```
