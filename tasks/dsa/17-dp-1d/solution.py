def climb_stairs(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    a, b = 1, 1  # ways(0), ways(1)
    for _ in range(n):
        a, b = b, a + b
    return a


def house_robber(loot):
    take, skip = 0, 0  # best totals if we do / don't rob the previous house
    for x in loot:
        take, skip = skip + x, max(take, skip)
    return max(take, skip)
