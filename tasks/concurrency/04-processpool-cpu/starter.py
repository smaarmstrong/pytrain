from concurrent.futures import ProcessPoolExecutor  # noqa: F401


def process_map(fn, items, max_workers=4):
    """Ordered results of fn(item) computed in worker processes."""
    raise NotImplementedError


def map_reduce(map_fn, reduce_fn, items, max_workers=4):
    """Map in worker processes, reduce (once, on the full ordered list)
    in this process."""
    raise NotImplementedError
