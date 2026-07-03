def permutations_of(items):
    if not items:
        return [[]]
    out = []
    for i in range(len(items)):
        rest = items[:i] + items[i + 1:]
        for perm in permutations_of(rest):
            out.append([items[i]] + perm)
    return out


def subsets_of(items):
    if not items:
        return [[]]
    rest = subsets_of(items[1:])
    return rest + [[items[0]] + s for s in rest]


def flatten(nested):
    out = []
    for x in nested:
        if isinstance(x, list):
            out.extend(flatten(x))
        else:
            out.append(x)
    return out
