"""Meta-grader: the bad implementations differ from the good one only in how
many times / how / when they call fetch — side_effect sequences plus call
assertions are the only way to tell them apart."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_sync.py"
TARGET_FILE = "sync.py"

GOOD = '''\
def fetch(url):
    raise RuntimeError("network access is disabled here — patch me in tests")


def fetch_with_retry(url, attempts=3):
    last = None
    for _ in range(attempts):
        try:
            return fetch(url)
        except ConnectionError as exc:
            last = exc
    raise last
'''


def _mutant(old, new):
    src = GOOD.replace(old, new)
    assert src != GOOD, f"mutant substitution failed: {old!r}"
    return src


BADS = {
    "one_extra_attempt": _mutant(
        "    for _ in range(attempts):",
        "    for _ in range(attempts + 1):",
    ),
    "never_retries": _mutant(
        "    last = None\n"
        "    for _ in range(attempts):\n"
        "        try:\n"
        "            return fetch(url)\n"
        "        except ConnectionError as exc:\n"
        "            last = exc\n"
        "    raise last",
        "    return fetch(url)",
    ),
    "returns_none_when_exhausted": _mutant(
        "    raise last",
        "    return None",
    ),
    "retries_every_exception": _mutant(
        "        except ConnectionError as exc:",
        "        except Exception as exc:",
    ),
    "passes_extra_argument": _mutant(
        "            return fetch(url)",
        "            return fetch(url, attempts)",
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
        "RuntimeError about network access you forgot to patch sync.fetch:\n"
        + tail(proc)
    )


@pytest.mark.parametrize("bug", sorted(BADS))
def test_your_tests_catch_each_bug(bug, tmp_path):
    proc = run_learner_tests(BADS[bug], tmp_path)
    if proc.returncode == 0:
        pytest.fail(f"a buggy implementation ({bug.replace('_', ' ')}) passed your "
                    "tests — script side_effect sequences and assert call counts/args")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against the '{bug}' "
                    f"implementation:\n{tail(proc)}")
