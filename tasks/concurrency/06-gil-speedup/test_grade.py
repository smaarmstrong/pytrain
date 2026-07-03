import importlib
import sys
import time

from pytrain_grader import load_solution, get_attr, workspace

# Workers cross process boundaries, so they live in a real importable
# module file in the workspace, not in this grader.
_HELPER_NAME = "_pytrain_gilworkers"
_HELPER_SRC = '''\
import time


def burn(n):
    """Pure-Python CPU grind: holds the GIL the whole time."""
    s = 0
    for i in range(n):
        s += i * i
    return s


def snooze(seconds):
    time.sleep(seconds)
'''


def _helpers():
    path = workspace() / (_HELPER_NAME + ".py")
    path.write_text(_HELPER_SRC)
    ws = str(workspace())
    if ws not in sys.path:
        sys.path.insert(0, ws)
    return importlib.import_module(_HELPER_NAME)


def _calibrated_n(burn):
    """Pick n so one burn(n) takes at least ~0.08s on this machine."""
    n = 200_000
    while n < 30_000_000:
        start = time.monotonic()
        burn(n)
        if time.monotonic() - start >= 0.08:
            break
        n *= 2
    return n


def test_threads_run_concurrently_and_are_waited_for():
    run_in_threads = get_attr(load_solution(), "run_in_threads")
    helpers = _helpers()
    elapsed = run_in_threads(helpers.snooze, 0.3, 4)
    assert isinstance(elapsed, float)
    # Must have waited for the sleeps (catches a missing join)...
    assert elapsed >= 0.25, f"returned after {elapsed:.2f}s — did you join?"
    # ...but overlapped them (sequential would be 1.2s).
    assert elapsed < 1.0, f"4 x 0.3s sleeps took {elapsed:.2f}s — not concurrent"


def test_processes_run_concurrently_and_are_waited_for():
    run_in_processes = get_attr(load_solution(), "run_in_processes")
    helpers = _helpers()
    elapsed = run_in_processes(helpers.snooze, 0.3, 4)
    assert isinstance(elapsed, float)
    assert elapsed >= 0.25, f"returned after {elapsed:.2f}s — did you wait/join?"
    assert elapsed < 1.0, f"4 x 0.3s sleeps took {elapsed:.2f}s — not concurrent"


def test_gil_speedup_on_cpu_bound_work():
    mod = load_solution()
    gil_speedup = get_attr(mod, "gil_speedup")
    helpers = _helpers()
    n = _calibrated_n(helpers.burn)
    speedup = gil_speedup(helpers.burn, n, 4)
    # Threads serialize CPU-bound Python (GIL): ~4x one call. Processes run
    # in parallel: ~1x plus startup. The ratio should be comfortably above
    # 1; we assert a deliberately loose 1.3 to stay robust under load.
    assert speedup >= 1.3, (
        f"gil_speedup={speedup:.2f} — processes should beat threads clearly "
        "on CPU-bound work; check that run_in_processes really uses "
        "processes and run_in_threads really uses threads"
    )
