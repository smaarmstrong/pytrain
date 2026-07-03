"""Meta-grader: every bad implementation returns None just like the good one —
only mock call assertions can discriminate. The real send_email raises, so
unpatched tests fail the good implementation too."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_alerts.py"
TARGET_FILE = "alerts.py"

GOOD = '''\
def send_email(to, subject, body):
    raise RuntimeError("email transport is disabled outside production — patch me")


def check_and_alert(stock, threshold):
    for name in sorted(stock):
        qty = stock[name]
        if qty < threshold:
            send_email("ops@example.com", f"Low stock: {name}", f"Only {qty} left")
'''


def _mutant(old, new):
    src = GOOD.replace(old, new)
    assert src != GOOD, f"mutant substitution failed: {old!r}"
    return src


BADS = {
    "alerts_at_threshold_too": _mutant(
        "        if qty < threshold:",
        "        if qty <= threshold:",
    ),
    "wrong_recipient": _mutant(
        '"ops@example.com"',
        '"admin@example.com"',
    ),
    "subject_missing_item_name": _mutant(
        'f"Low stock: {name}"',
        '"Low stock"',
    ),
    "only_first_low_item": _mutant(
        '            send_email("ops@example.com", f"Low stock: {name}", f"Only {qty} left")',
        '            send_email("ops@example.com", f"Low stock: {name}", f"Only {qty} left")\n'
        "            break",
    ),
    "one_batch_email": _mutant(
        "def check_and_alert(stock, threshold):\n"
        "    for name in sorted(stock):\n"
        "        qty = stock[name]\n"
        "        if qty < threshold:\n"
        '            send_email("ops@example.com", f"Low stock: {name}", f"Only {qty} left")',
        "def check_and_alert(stock, threshold):\n"
        "    low = [name for name in sorted(stock) if stock[name] < threshold]\n"
        "    if low:\n"
        '        send_email("ops@example.com", "Low stock: " + ", ".join(low),\n'
        '                   f"{len(low)} items low")',
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
        "RuntimeError about the email transport you forgot to patch "
        "alerts.send_email:\n" + tail(proc)
    )


@pytest.mark.parametrize("bug", sorted(BADS))
def test_your_tests_catch_each_bug(bug, tmp_path):
    proc = run_learner_tests(BADS[bug], tmp_path)
    if proc.returncode == 0:
        pytest.fail(f"a buggy implementation ({bug.replace('_', ' ')}) passed your "
                    "tests — assert on the mock's calls (count, args, order)")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against the '{bug}' "
                    f"implementation:\n{tail(proc)}")
