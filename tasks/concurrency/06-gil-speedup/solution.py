import multiprocessing
import threading
import time


def run_in_threads(fn, arg, n_workers):
    threads = [threading.Thread(target=fn, args=(arg,)) for _ in range(n_workers)]
    start = time.monotonic()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.monotonic() - start


def run_in_processes(fn, arg, n_workers):
    procs = [multiprocessing.Process(target=fn, args=(arg,)) for _ in range(n_workers)]
    start = time.monotonic()
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    return time.monotonic() - start


def gil_speedup(fn, arg, n_workers):
    return run_in_threads(fn, arg, n_workers) / run_in_processes(fn, arg, n_workers)
