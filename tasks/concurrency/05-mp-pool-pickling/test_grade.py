import importlib
import math
import os
import sys
import threading

import pytest

from pytrain_grader import load_solution, get_attr, workspace

# Pool pickles the callable by qualified name, so probes live in a real
# module file in the workspace (importable in parent and worker processes).
_HELPER_NAME = "_pytrain_procworkers05"
_HELPER_SRC = '''\
import os
import time


def double(x):
    return x * 2


def pid_tag(x):
    time.sleep(0.05)      # keep each worker busy so the pool fans out
    return (os.getpid(), x)
'''


def _helpers():
    path = workspace() / (_HELPER_NAME + ".py")
    path.write_text(_HELPER_SRC)
    ws = str(workspace())
    if ws not in sys.path:
        sys.path.insert(0, ws)
    return importlib.import_module(_HELPER_NAME)


def test_pool_map_ordered_results():
    pool_map = get_attr(load_solution(), "pool_map")
    helpers = _helpers()
    assert pool_map(helpers.double, [3, 1, 2], processes=2) == [6, 2, 4]
    assert pool_map(math.factorial, [5, 0, 3], processes=2) == [120, 1, 6]


def test_pool_map_spreads_across_worker_processes():
    pool_map = get_attr(load_solution(), "pool_map")
    helpers = _helpers()
    results = pool_map(helpers.pid_tag, list(range(8)), processes=4)
    pids = {pid for pid, _ in results}
    tags = [tag for _, tag in results]
    assert tags == list(range(8)), "results not in input order"
    assert os.getpid() not in pids, "work ran in the parent process"
    assert len(pids) >= 2, f"only one worker pid seen ({pids})"


def test_pool_map_unpicklable_function_raises():
    pool_map = get_attr(load_solution(), "pool_map")
    with pytest.raises(Exception):
        pool_map(lambda x: x, [1, 2, 3], processes=2)


def test_is_picklable():
    is_picklable = get_attr(load_solution(), "is_picklable")
    assert is_picklable(42) is True
    assert is_picklable("hello") is True
    assert is_picklable([1, (2, 3), {"k": "v"}]) is True
    assert is_picklable(math.sqrt) is True          # named module-level fn
    assert is_picklable(lambda x: x) is False
    assert is_picklable(threading.Lock()) is False
    assert is_picklable((i for i in range(3))) is False


def test_split_picklable_partitions_in_order():
    split_picklable = get_attr(load_solution(), "split_picklable")
    fn = lambda x: x  # noqa: E731
    lock = threading.Lock()
    gen = (i for i in range(3))
    objs = [1, fn, "a", lock, (2, 3), gen, {"k": 1}]
    good, bad = split_picklable(objs)
    assert good == [1, "a", (2, 3), {"k": 1}]
    assert bad[0] is fn and bad[1] is lock and bad[2] is gen
    assert len(bad) == 3


def test_split_picklable_empty_and_all_good():
    split_picklable = get_attr(load_solution(), "split_picklable")
    assert split_picklable([]) == ([], [])
    good, bad = split_picklable([1, 2])
    assert good == [1, 2] and bad == []
