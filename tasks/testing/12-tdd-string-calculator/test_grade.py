"""Grader: runs the kata's GIVEN suite (our own copy — editing the workspace
copy doesn't help) against the learner's solution.py, then hidden edge-case
tests drawn from the same contract."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import get_attr, load_solution, workspace

GIVEN_SUITE = '''\
import pytest

from solution import add


def test_empty_string_is_zero():
    assert add("") == 0


def test_single_number():
    assert add("5") == 5


def test_two_numbers_comma_separated():
    assert add("1,2") == 3


def test_many_numbers():
    assert add("1,2,3,10") == 16


def test_newlines_count_as_separators_too():
    assert add("1\\n2,3") == 6


def test_custom_delimiter_header():
    assert add("//;\\n1;2") == 3


def test_negatives_are_rejected_and_all_listed():
    with pytest.raises(ValueError, match="negatives not allowed: -2, -4"):
        add("1,-2,3,-4")
'''


def test_the_given_suite_passes(tmp_path):
    learner = workspace() / "solution.py"
    if not learner.exists():
        pytest.fail("solution.py not found in your workspace")
    (tmp_path / "solution.py").write_text(learner.read_text())
    (tmp_path / "test_calc.py").write_text(GIVEN_SUITE)
    env = os.environ.copy()
    env.pop("PYTEST_ADDOPTS", None)
    env.pop("PYTEST_PLUGINS", None)
    env["PYTHONPATH"] = str(tmp_path)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(tmp_path), "-q",
         "-p", "no:cacheprovider"],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=90,
    )
    assert proc.returncode == 0, (
        "the given suite (test_calc.py) does not pass yet:\n"
        + (proc.stdout + proc.stderr)[-1500:]
    )


# ---- hidden edge cases (same contract as the prompt) ------------------------

def _add():
    return get_attr(load_solution(), "add")


def test_multi_digit_numbers():
    add = _add()
    assert add("10,20,30") == 60
    assert add("7") == 7


def test_newlines_only():
    add = _add()
    assert add("1\n2\n3") == 6


def test_regex_special_custom_delimiters():
    add = _add()
    assert add("//*\n2*3*4") == 9
    assert add("//.\n1.2.3") == 6


def test_custom_delimiter_with_a_single_number():
    add = _add()
    assert add("//;\n8") == 8


def test_lone_negative_listed_in_message():
    add = _add()
    with pytest.raises(ValueError, match="negatives not allowed: -5"):
        add("-5")


def test_negatives_behind_a_custom_delimiter():
    add = _add()
    with pytest.raises(ValueError, match="negatives not allowed: -2, -3"):
        add("//;\n1;-2;-3")


def test_result_is_an_int():
    add = _add()
    assert isinstance(add("1,2"), int)
    assert isinstance(add(""), int)
