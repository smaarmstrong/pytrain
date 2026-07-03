import importlib
import math
import sys

from pytrain_grader import load_solution, get_attr, workspace

# Worker functions sent to child processes must be picklable, i.e. live in
# an importable module. The learner's solution module is loaded from a file
# path under a synthetic name, so we ship our probes in a real module file
# placed in the workspace (which is on sys.path in parent and children).
_HELPER_NAME = "_pytrain_procworkers04"
_HELPER_SRC = '''\
import os
import time


def square(x):
    return x * x


def pid_square(x):
    time.sleep(0.1)          # hold the worker so several processes get used
    return (os.getpid(), x * x)


def burn(n):
    s = 0
    for i in range(n):
        s += i * i
    return s
'''


def _helpers():
    path = workspace() / (_HELPER_NAME + ".py")
    path.write_text(_HELPER_SRC)
    ws = str(workspace())
    if ws not in sys.path:
        sys.path.insert(0, ws)
    return importlib.import_module(_HELPER_NAME)


def test_process_map_ordered_results():
    process_map = get_attr(load_solution(), "process_map")
    helpers = _helpers()
    assert process_map(helpers.square, [3, 1, 4, 1, 5], max_workers=2) == [9, 1, 16, 1, 25]
    assert process_map(math.factorial, [5, 3, 0], max_workers=2) == [120, 6, 1]


def test_process_map_empty():
    process_map = get_attr(load_solution(), "process_map")
    assert process_map(math.factorial, [], max_workers=2) == []


def test_work_runs_in_multiple_worker_processes():
    import os
    process_map = get_attr(load_solution(), "process_map")
    helpers = _helpers()
    results = process_map(helpers.pid_square, list(range(8)), max_workers=4)
    pids = {pid for pid, _ in results}
    squares = [sq for _, sq in results]
    assert squares == [x * x for x in range(8)], "results not in input order"
    assert os.getpid() not in pids, (
        "fn ran in the parent process — use worker processes"
    )
    assert len(pids) >= 2, (
        f"all 8 jobs ran in one process (pids={pids}) — the pool isn't "
        "spreading CPU-bound work across workers"
    )


def test_cpu_bound_correctness():
    process_map = get_attr(load_solution(), "process_map")
    helpers = _helpers()
    n = 50_000
    expected = sum(i * i for i in range(n))
    assert process_map(helpers.burn, [n, n], max_workers=2) == [expected, expected]


def test_map_reduce():
    map_reduce = get_attr(load_solution(), "map_reduce")
    helpers = _helpers()
    assert map_reduce(math.factorial, sum, [1, 2, 3], max_workers=2) == 9
    assert map_reduce(helpers.square, max, [3, 7, 2], max_workers=2) == 49
    # reduce_fn sees the ordered list, so order-sensitive reductions work
    assert map_reduce(helpers.square, lambda xs: xs, [2, 3], max_workers=2) == [4, 9]
