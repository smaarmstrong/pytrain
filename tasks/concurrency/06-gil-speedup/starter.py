import multiprocessing  # noqa: F401
import threading        # noqa: F401
import time             # noqa: F401


def run_in_threads(fn, arg, n_workers):
    """Elapsed seconds to run fn(arg) once per thread, n_workers threads
    concurrently."""
    raise NotImplementedError


def run_in_processes(fn, arg, n_workers):
    """Elapsed seconds to run fn(arg) once per process, n_workers processes
    concurrently."""
    raise NotImplementedError


def gil_speedup(fn, arg, n_workers):
    """threads time / processes time."""
    raise NotImplementedError
