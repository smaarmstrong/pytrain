def dedupe(items):
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def common_elements(a, b):
    return sorted(set(a) & set(b))


def first_unique_window(items, k):
    if k <= 0:
        raise ValueError("k must be positive")
    if k > len(items):
        return -1
    counts = {}
    distinct = 0
    for j, x in enumerate(items):
        counts[x] = counts.get(x, 0) + 1
        if counts[x] == 1:
            distinct += 1
        if j >= k:
            old = items[j - k]
            counts[old] -= 1
            if counts[old] == 0:
                distinct -= 1
        if j >= k - 1 and distinct == k:
            return j - k + 1
    return -1
