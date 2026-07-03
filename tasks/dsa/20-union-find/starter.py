class DisjointSet:
    """Union-find over arbitrary hashable elements. See prompt.md."""

    def add(self, x):
        raise NotImplementedError

    def find(self, x):
        raise NotImplementedError

    def union(self, a, b):
        raise NotImplementedError

    def connected(self, a, b):
        raise NotImplementedError


def count_components(n, edges):
    """Connected groups among nodes 0..n-1 under undirected `edges`."""
    raise NotImplementedError
