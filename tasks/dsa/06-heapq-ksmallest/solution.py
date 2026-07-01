import heapq


def k_smallest(items, k):
    """Keep a max-heap (negated values) of the k smallest seen so far."""
    if k <= 0:
        return []
    heap = []  # stores -value, so heap[0] is the largest of the kept k
    for x in items:
        if len(heap) < k:
            heapq.heappush(heap, -x)
        elif x < -heap[0]:
            heapq.heapreplace(heap, -x)
    return sorted(-v for v in heap)
