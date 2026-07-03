"""Meta-grader: the learner's suite must pin down exception types, messages
and warning categories — each bad implementation gets exactly one wrong."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_bank.py"
TARGET_FILE = "bank.py"

GOOD = '''\
import warnings


class InsufficientFunds(Exception):
    pass


def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFunds(f"short by {amount - balance}")
    return balance - amount


def take(balance, amount):
    warnings.warn("take is deprecated; use withdraw", DeprecationWarning, stacklevel=2)
    return withdraw(balance, amount)
'''


def _mutant(old, new):
    src = GOOD.replace(old, new)
    assert src != GOOD, f"mutant substitution failed: {old!r}"
    return src


BADS = {
    "wrong_valueerror_message": _mutant(
        'raise ValueError("amount must be positive")',
        'raise ValueError("invalid amount")',
    ),
    "wrong_exception_type_for_overdraft": _mutant(
        'raise InsufficientFunds(f"short by {amount - balance}")',
        'raise ValueError(f"short by {amount - balance}")',
    ),
    "wrong_shortfall_amount": _mutant(
        'raise InsufficientFunds(f"short by {amount - balance}")',
        'raise InsufficientFunds(f"short by {amount}")',
    ),
    "zero_amount_allowed": _mutant(
        "    if amount <= 0:",
        "    if amount < 0:",
    ),
    "no_deprecation_warning": _mutant(
        '    warnings.warn("take is deprecated; use withdraw", DeprecationWarning, stacklevel=2)\n',
        "",
    ),
    "wrong_warning_category": _mutant(
        "DeprecationWarning, stacklevel=2",
        "UserWarning, stacklevel=2",
    ),
    "does_not_deduct": _mutant(
        "    return balance - amount",
        "    return balance",
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
        "your tests must all PASS against a correct implementation, but:\n" + tail(proc)
    )


@pytest.mark.parametrize("bug", sorted(BADS))
def test_your_tests_catch_each_bug(bug, tmp_path):
    proc = run_learner_tests(BADS[bug], tmp_path)
    if proc.returncode == 0:
        pytest.fail(f"a buggy implementation ({bug.replace('_', ' ')}) passed your "
                    "tests — pin down types, messages and categories with match=")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against the '{bug}' "
                    f"implementation:\n{tail(proc)}")
