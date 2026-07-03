class DisjointSet:
    def __init__(self):
        self._parent = {}
        self._size = {}

    def add(self, x):
        if x not in self._parent:
            self._parent[x] = x
            self._size[x] = 1

    def find(self, x):
        root = self._parent[x]  # KeyError for unknown x, as specified
        while self._parent[root] != root:
            root = self._parent[root]
        # path compression
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a, b):
        self.add(a)
        self.add(b)
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]
        return True

    def connected(self, a, b):
        if a not in self._parent or b not in self._parent:
            return False
        return self.find(a) == self.find(b)


def count_components(n, edges):
    ds = DisjointSet()
    for node in range(n):
        ds.add(node)
    count = n
    for u, v in edges:
        if ds.union(u, v):
            count -= 1
    return count
