import queue      # noqa: F401
import threading  # noqa: F401


def run_pipeline(items, process, n_workers):
    """Fan items out to n_workers consumer threads via a queue.Queue.

    Return the list of process(item) results (any order). All worker
    threads must be finished before returning.
    """
    raise NotImplementedError
