import threading
import time

from pytrain_grader import load_solution, get_attr


class Probe:
    """A counter whose read is slow, so an unlocked read-modify-write
    reliably loses updates under concurrency."""

    def __init__(self):
        self._v = 0
        self.writer_idents = set()

    def read(self):
        v = self._v
        time.sleep(0.001)  # widen the race window
        return v

    def write(self, v):
        self.writer_idents.add(threading.get_ident())
        self._v = v


def _funcs():
    mod = load_solution()
    return get_attr(mod, "increment_many"), get_attr(mod, "run_workers")


def test_single_thread_counts_correctly():
    increment_many, _ = _funcs()
    probe = Probe()
    increment_many(probe, threading.Lock(), 7)
    assert probe.read() == 7


def test_no_updates_lost_under_contention():
    _, run_workers = _funcs()
    probe = Probe()
    result = run_workers(probe, threading.Lock(), n_threads=4, times_per_thread=10)
    assert result == 40, (
        "updates were lost — is the WHOLE read-modify-write inside the lock?"
    )
    assert probe.read() == 40


def test_heavier_contention_still_exact():
    _, run_workers = _funcs()
    probe = Probe()
    result = run_workers(probe, threading.Lock(), n_threads=8, times_per_thread=15)
    assert result == 120


def test_work_happens_on_n_new_threads():
    _, run_workers = _funcs()
    probe = Probe()
    main_ident = threading.get_ident()
    run_workers(probe, threading.Lock(), n_threads=4, times_per_thread=3)
    assert main_ident not in probe.writer_idents, (
        "increments ran on the calling thread — spawn worker threads instead"
    )
    assert len(probe.writer_idents) == 4, (
        f"expected 4 distinct worker threads, saw {len(probe.writer_idents)}"
    )


def test_workers_are_joined_before_return():
    _, run_workers = _funcs()
    probe = Probe()
    before = {t.ident for t in threading.enumerate()}
    result = run_workers(probe, threading.Lock(), n_threads=3, times_per_thread=5)
    # If workers weren't joined, the returned count would be short and/or
    # worker threads would still be alive here.
    assert result == 15
    leftovers = [t for t in threading.enumerate()
                 if t.ident not in before and t.is_alive()]
    assert not leftovers, "worker threads still running after run_workers returned"
