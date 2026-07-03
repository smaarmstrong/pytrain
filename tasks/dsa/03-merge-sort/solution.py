def merge(left, right, key=None):
    k = key if key is not None else (lambda x: x)
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if k(right[j]) < k(left[i]):
            out.append(right[j])
            j += 1
        else:  # left wins ties -> stability
            out.append(left[i])
            i += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_sort(items, key=None):
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    return merge(merge_sort(items[:mid], key), merge_sort(items[mid:], key), key)
