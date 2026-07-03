"""Meta-grader: the learner's suite must pass TWO correct implementations
that sum in different orders (killing exact float equality) and fail each
buggy one (all wrong by far more than the 1e-6 contract)."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_stats.py"
TARGET_FILE = "stats.py"

GOOD_ONE_PASS = '''\
def mean(xs):
    if not xs:
        raise ValueError("empty data")
    return sum(xs) / len(xs)


def variance(xs):
    if not xs:
        raise ValueError("empty data")
    n = len(xs)
    m = sum(xs) / n
    return sum(x * x for x in xs) / n - m * m


def normalize(xs):
    total = sum(xs)
    if total == 0:
        raise ValueError("cannot normalize: sum is zero")
    return [x / total for x in xs]
'''

GOOD_TWO_PASS_FSUM = '''\
import math


def mean(xs):
    if not xs:
        raise ValueError("empty data")
    return math.fsum(xs) / len(xs)


def variance(xs):
    if not xs:
        raise ValueError("empty data")
    m = mean(xs)
    return math.fsum((x - m) ** 2 for x in xs) / len(xs)


def normalize(xs):
    total = math.fsum(xs)
    if total == 0:
        raise ValueError("cannot normalize: sum is zero")
    return [x / total for x in xs]
'''

GOODS = {"one_pass_sum": GOOD_ONE_PASS, "two_pass_fsum": GOOD_TWO_PASS_FSUM}


def _mutant(old, new):
    src = GOOD_ONE_PASS.replace(old, new)
    assert src != GOOD_ONE_PASS, f"mutant substitution failed: {old!r}"
    return src


BADS = {
    "sample_variance_not_population": _mutant(
        "    return sum(x * x for x in xs) / n - m * m",
        "    return sum((x - m) ** 2 for x in xs) / (n - 1)",
    ),
    "normalizes_by_max": _mutant(
        "    total = sum(xs)",
        "    total = max(xs)",
    ),
    "mean_drops_first_value": _mutant(
        "    return sum(xs) / len(xs)",
        "    return sum(xs[1:]) / len(xs[1:])",
    ),
    "mean_of_empty_returns_zero": _mutant(
        'def mean(xs):\n    if not xs:\n        raise ValueError("empty data")\n',
        "def mean(xs):\n    if not xs:\n        return 0.0\n",
    ),
    "normalize_zero_sum_zerodivision": _mutant(
        '    if total == 0:\n        raise ValueError("cannot normalize: sum is zero")\n',
        "",
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


@pytest.mark.parametrize("variant", sorted(GOODS))
def test_your_tests_pass_both_correct_implementations(variant, tmp_path):
    proc = run_learner_tests(GOODS[variant], tmp_path)
    assert proc.returncode == 0, (
        f"your tests must PASS any implementation accurate to 1e-6, but failed the "
        f"'{variant}' variant — are you comparing floats with == instead of "
        f"pytest.approx?\n" + tail(proc)
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
