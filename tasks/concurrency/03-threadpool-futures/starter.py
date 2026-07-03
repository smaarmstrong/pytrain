from concurrent.futures import ThreadPoolExecutor, as_completed  # noqa: F401


def parallel_map(fn, items, max_workers):
    """Ordered results via executor.map; exceptions propagate."""
    raise NotImplementedError


def try_map(fn, items, max_workers):
    """submit() each item; return {item: ("ok", result) | ("error", exc_name)}."""
    raise NotImplementedError


def first_result(fn, items, max_workers):
    """Return the result of whichever fn(item) call finishes first."""
    raise NotImplementedError
