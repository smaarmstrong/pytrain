def flatten(items):
    """Lazily yield the leaves of arbitrarily nested lists/tuples.

    Strings (and everything else that isn't a list/tuple) are leaves.
    """
    raise NotImplementedError


def chunk_sum(chunk):
    """Yield each number in chunk; return (not yield) their sum."""
    raise NotImplementedError


def stream_sums(chunks):
    """Yield every number of every chunk in order; return the list of
    per-chunk sums (collect them from `yield from chunk_sum(...)`)."""
    raise NotImplementedError
