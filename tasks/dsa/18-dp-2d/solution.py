def grid_paths(rows, cols, blocked=()):
    blocked = set(blocked)
    if (0, 0) in blocked or (rows - 1, cols - 1) in blocked:
        return 0
    row = [0] * cols
    row[0] = 1
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked:
                row[c] = 0
            elif c > 0:
                row[c] += row[c - 1]
    return row[-1]


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(
                prev[j] + 1,        # delete ca
                cur[j - 1] + 1,     # insert cb
                prev[j - 1] + (ca != cb),  # substitute (or keep)
            )
        prev = cur
    return prev[-1]


def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0] * (len(b) + 1)
        for j, cb in enumerate(b, 1):
            cur[j] = prev[j - 1] + 1 if ca == cb else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]
