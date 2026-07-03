import threading  # noqa: F401  (you will need it)


def increment_many(probe, lock, times):
    """Increment the probe `times` times, locking each read-modify-write."""
    raise NotImplementedError


def run_workers(probe, lock, n_threads, times_per_thread):
    """Run increment_many on n_threads new threads, join them all,
    return probe.read()."""
    raise NotImplementedError
