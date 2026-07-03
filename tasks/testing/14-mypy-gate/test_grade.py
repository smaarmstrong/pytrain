"""Grader: mypy with the strict-ish flags from the prompt must exit clean on
the learner's solution.py AND every function must still behave as specified."""
import subprocess
import sys

import pytest

from pytrain_grader import get_attr, load_solution, workspace

MYPY_FLAGS = [
    "--disallow-untyped-defs",
    "--disallow-incomplete-defs",
    "--no-implicit-optional",
    "--warn-return-any",
]


def test_mypy_gate_is_green(tmp_path):
    target = workspace() / "solution.py"
    if not target.exists():
        pytest.fail("solution.py not found in your workspace")
    proc = subprocess.run(
        [sys.executable, "-m", "mypy", "--no-error-summary", "--soft-error-limit=-1",
         "--cache-dir", str(tmp_path / ".mypy_cache"), *MYPY_FLAGS, str(target)],
        capture_output=True, text=True, cwd=str(workspace()), timeout=120,
    )
    assert proc.returncode == 0, (
        "mypy is not clean under " + " ".join(MYPY_FLAGS) + ":\n"
        + proc.stdout + proc.stderr
    )


def test_mean_behaviour_unchanged():
    f = get_attr(load_solution(), "mean")
    assert f([2.0, 4.0]) == 3.0
    assert f([1.5]) == 1.5
    with pytest.raises(ValueError):
        f([])


def test_lookup_behaviour_unchanged():
    f = get_attr(load_solution(), "lookup")
    assert f({"ada": 97, "alan": 88}, "ada") == 97
    assert f({"ada": 97}, "grace") is None
    assert f({"ada": 97}, "grace", 50) == 50


def test_repeat_behaviour_unchanged():
    f = get_attr(load_solution(), "repeat")
    assert f("hi") == "hi hi"
    assert f("x", 3) == "x x x"
    assert f("once", 1) == "once"


def test_first_long_word_behaviour_unchanged():
    f = get_attr(load_solution(), "first_long_word")
    assert f(["a", "abc", "abcdef"], 3) == "abc"
    assert f(["ab"], 5) is None
    assert f([], 1) is None
