def make_cached(fn):
    """Return a memoised wrapper around fn (positional, hashable args)."""
    raise NotImplementedError


def int_parser(base):
    """Return a function parsing strings as integers in `base`."""
    raise NotImplementedError


def fib(n):
    """n-th Fibonacci number; memoised recursion (fib(200) must be instant)."""
    raise NotImplementedError
