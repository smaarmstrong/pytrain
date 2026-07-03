from collections.abc import Sequence

# Rewrite these with PEP 695 type-parameter syntax: def pick[T](...) etc.


def pick(items, index):
    raise NotImplementedError


def swap(pair):
    raise NotImplementedError


class Pair:
    def __init__(self, first, second):
        raise NotImplementedError
