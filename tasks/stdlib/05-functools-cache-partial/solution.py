from functools import cache, lru_cache, partial


def make_cached(fn):
    return lru_cache(maxsize=None)(fn)


def int_parser(base):
    return partial(int, base=base)


@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
