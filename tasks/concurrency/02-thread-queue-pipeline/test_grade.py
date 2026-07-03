import threading
import time
from collections import Counter

from pytrain_grader import load_solution, get_attr


def _run_pipeline():
    return get_attr(load_solution(), "run_pipeline")


def test_every_item_processed_exactly_once():
    run_pipeline = _run_pipeline()
    out = run_pipeline([1, 2, 3, 4, 5], lambda x: x * 10, n_workers=2)
    assert Counter(out) == Counter([10, 20, 30, 40, 50])


def test_duplicates_and_single_worker():
    run_pipeline = _run_pipeline()
    out = run_pipeline([2, 2, 2], lambda x: x + 1, n_workers=1)
    assert Counter(out) == Counter([3, 3, 3])


def test_empty_items():
    run_pipeline = _run_pipeline()
    assert run_pipeline([], str, n_workers=4) == []


def test_more_workers_than_items():
    run_pipeline = _run_pipeline()
    out = run_pipeline(["a", "b"], str.upper, n_workers=8)
    assert Counter(out) == Counter(["A", "B"])


def test_workers_overlap_the_waits():
    run_pipeline = _run_pipeline()
    idents = set()
    idents_lock = threading.Lock()

    def slow(x):
        with idents_lock:
            idents.add(threading.get_ident())
        time.sleep(0.2)
        return x

    start = time.monotonic()
    out = run_pipeline(list(range(8)), slow, n_workers=4)
    elapsed = time.monotonic() - start
    assert Counter(out) == Counter(range(8))
    # 4 workers x 2 rounds of 0.2s sleeps: ideal ~0.4s, sequential = 1.6s.
    assert elapsed < 1.2, (
        f"took {elapsed:.2f}s for 8 x 0.2s jobs on 4 workers — "
        "workers are not running concurrently"
    )
    assert len(idents) >= 2, "all items were processed by a single thread"


def test_all_workers_terminated_on_return():
    run_pipeline = _run_pipeline()
    before = {t.ident for t in threading.enumerate()}
    run_pipeline(list(range(6)), lambda x: x, n_workers=3)
    leftovers = [t for t in threading.enumerate()
                 if t.ident not in before and t.is_alive()]
    assert not leftovers, (
        "worker threads still alive after run_pipeline returned — "
        "shut the crew down (sentinels or join) before returning"
    )
