"""Meta-grader: the learner's fixture-based suite must pass a correct kvstore
and fail each buggy one. The one-open-store rule means a suite without
reliable teardown fails the correct implementation too."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_kvstore.py"
TARGET_FILE = "kvstore.py"

GOOD = '''\
_open_count = 0


class StoreClosed(Exception):
    pass


def connect():
    global _open_count
    if _open_count >= 1:
        raise RuntimeError("an open store already exists — close it first")
    _open_count += 1
    return Store()


class Store:
    def __init__(self):
        self._data = {}
        self._closed = False

    def _check_open(self):
        if self._closed:
            raise StoreClosed("store is closed")

    def put(self, key, value):
        self._check_open()
        self._data[key] = value

    def get(self, key):
        self._check_open()
        return self._data[key]

    def delete(self, key):
        self._check_open()
        if key in self._data:
            del self._data[key]
            return True
        return False

    def close(self):
        global _open_count
        if not self._closed:
            self._closed = True
            _open_count -= 1
'''


def _mutant(old, new):
    src = GOOD.replace(old, new)
    assert src != GOOD, f"mutant substitution failed: {old!r}"
    return src


BADS = {
    "put_does_not_overwrite": _mutant(
        "        self._data[key] = value",
        "        self._data.setdefault(key, value)",
    ),
    "get_missing_returns_none": _mutant(
        "        return self._data[key]",
        "        return self._data.get(key)",
    ),
    "delete_missing_raises": _mutant(
        "        if key in self._data:\n"
        "            del self._data[key]\n"
        "            return True\n"
        "        return False",
        "        del self._data[key]\n"
        "        return True",
    ),
    "usable_after_close": _mutant(
        "        if not self._closed:\n"
        "            self._closed = True\n"
        "            _open_count -= 1",
        "        if not self._closed:\n"
        "            _open_count -= 1",
    ),
}


def run_learner_tests(impl_src, tmp_path, extra=()):
    learner = workspace() / TEST_FILE
    if not learner.exists():
        pytest.fail(f"{TEST_FILE} not found in your workspace")
    (tmp_path / TARGET_FILE).write_text(impl_src)
    (tmp_path / TEST_FILE).write_text(learner.read_text())
    env = os.environ.copy()
    env.pop("PYTEST_ADDOPTS", None)
    env.pop("PYTEST_PLUGINS", None)
    env["PYTHONPATH"] = str(tmp_path)
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(tmp_path), "-q",
         "-p", "no:cacheprovider", *extra],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=90,
    )


def tail(proc):
    return (proc.stdout + proc.stderr)[-1500:]


def test_your_tests_pass_a_correct_implementation(tmp_path):
    proc = run_learner_tests(GOOD, tmp_path)
    assert proc.returncode == 0, (
        "your tests must all PASS against a correct implementation — if you see "
        "RuntimeError('an open store already exists') your fixtures are leaking "
        "open stores (close in teardown!):\n" + tail(proc)
    )


@pytest.mark.parametrize("bug", sorted(BADS))
def test_your_tests_catch_each_bug(bug, tmp_path):
    proc = run_learner_tests(BADS[bug], tmp_path)
    if proc.returncode == 0:
        pytest.fail(f"a buggy implementation ({bug.replace('_', ' ')}) passed your "
                    "tests — add a test that catches it (see the spec)")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against the '{bug}' "
                    f"implementation:\n{tail(proc)}")
