import threading
import time

import pytest

from pytrain_grader import load_solution, get_attr


def _mod():
    return load_solution()


def test_parallel_map_ordered_results():
    f = get_attr(_mod(), "parallel_map")
    assert f(str.upper, ["a", "b", "c"], 2) == ["A", "B", "C"]
    assert f(lambda x: x * x, [3, 1, 2], 3) == [9, 1, 4]
    assert f(str, [], 2) == []


def test_parallel_map_runs_concurrently():
    f = get_attr(_mod(), "parallel_map")
    idents = set()
    lock = threading.Lock()

    def slow(x):
        with lock:
            idents.add(threading.get_ident())
        time.sleep(0.3)
        return x * 2

    start = time.monotonic()
    out = f(slow, [1, 2, 3, 4, 5], 5)
    elapsed = time.monotonic() - start
    assert out == [2, 4, 6, 8, 10]
    # ideal ~0.3s, sequential = 1.5s
    assert elapsed < 1.0, (
        f"5 x 0.3s calls with 5 workers took {elapsed:.2f}s — not concurrent"
    )
    assert len(idents) >= 2


def test_parallel_map_propagates_exception():
    f = get_attr(_mod(), "parallel_map")

    def boom(x):
        if x == 2:
            raise ValueError("bad item")
        return x

    with pytest.raises(ValueError):
        f(boom, [1, 2, 3], 2)


def test_try_map_captures_ok_and_errors():
    f = get_attr(_mod(), "try_map")
    out = f(lambda x: 10 // x, [1, 0, 2, 5], 3)
    assert out == {
        1: ("ok", 10),
        0: ("error", "ZeroDivisionError"),
        2: ("ok", 5),
        5: ("ok", 2),
    }


def test_try_map_mixed_exception_types():
    f = get_attr(_mod(), "try_map")

    def picky(x):
        if x == "k":
            raise KeyError(x)
        if x == "v":
            raise ValueError(x)
        return x.upper()

    out = f(picky, ["a", "k", "v"], 2)
    assert out == {
        "a": ("ok", "A"),
        "k": ("error", "KeyError"),
        "v": ("error", "ValueError"),
    }


def test_first_result_returns_the_fast_one():
    f = get_attr(_mod(), "first_result")

    def sleepy(d):
        time.sleep(d)
        return d

    # 0.05s vs 1.5s: a 30x gap — the fast one wins by a mile.
    start = time.monotonic()
    got = f(sleepy, [1.5, 0.05, 1.5], 3)
    elapsed = time.monotonic() - start
    assert got == 0.05
    assert elapsed < 0.5, (
        f"first_result took {elapsed:.2f}s — it must return as soon as the "
        "first future completes, not wait for the slow ones "
        "(hint: the executor's context manager waits on exit)"
    )
