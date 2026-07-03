"""Grader: `ruff check` (default rules) must exit clean on the learner's
solution.py AND every function must still behave exactly as before."""
import subprocess
import sys

import pytest

from pytrain_grader import get_attr, load_solution, workspace


def test_ruff_check_is_clean():
    target = workspace() / "solution.py"
    if not target.exists():
        pytest.fail("solution.py not found in your workspace")
    proc = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--no-cache", "--isolated",
         str(target)],
        capture_output=True, text=True, cwd=str(workspace()), timeout=60,
    )
    assert proc.returncode == 0, (
        "`ruff check` still reports violations:\n" + proc.stdout + proc.stderr
    )


def test_subtotal_behaviour_unchanged():
    f = get_attr(load_solution(), "subtotal")
    assert f([]) == 0
    assert f([1.5, 2.5, 6.0]) == 10.0
    assert f([4]) == 4


def test_apply_discount_behaviour_unchanged():
    f = get_attr(load_solution(), "apply_discount")
    assert f(100.0, None) == 100.0
    assert f(100.0, "HALF") == 50.0
    assert f(100.0, "25") == 75.0
    assert f(100.0, "FREESHIP") == 100.0
    assert f(80.0, "10") == 72.0


def test_summary_behaviour_unchanged():
    f = get_attr(load_solution(), "summary")
    assert f([10.0, 5.555]) == "TOTAL: 15.55"
    assert f([10.0], "HALF") == "TOTAL: 5.0"
    assert f([], None) == "TOTAL: 0.0"
