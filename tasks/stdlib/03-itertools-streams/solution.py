from itertools import chain, groupby, islice, pairwise


def take(iterable, n):
    return list(islice(iterable, n))


def flatten(iterables):
    return list(chain.from_iterable(iterables))


def runs(iterable):
    return [(value, sum(1 for _ in group)) for value, group in groupby(iterable)]


def deltas(iterable):
    return [b - a for a, b in pairwise(iterable)]
