def take(iterable, n):
    """First n items as a list; must cope with infinite iterables."""
    raise NotImplementedError


def flatten(iterables):
    """Chain all inner iterables into one list (one level deep)."""
    raise NotImplementedError


def runs(iterable):
    """Run-length encode consecutive equal values as (value, count) tuples."""
    raise NotImplementedError


def deltas(iterable):
    """Differences between consecutive items."""
    raise NotImplementedError
