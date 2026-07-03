import subprocess
import sys

import pytest

from pytrain_grader import load_solution, get_attr, workspace


def _mypy(target, *flags):
    return subprocess.run(
        [sys.executable, "-m", "mypy", "--no-error-summary", "--soft-error-limit=-1",
         *flags, str(target)],
        capture_output=True, text=True, cwd=str(workspace()),
    )


# ---- behaviour --------------------------------------------------------------

def test_is_str_list():
    f = get_attr(load_solution(), "is_str_list")
    assert f(["a", "b"]) is True
    assert f([]) is True
    assert f(["a", 1]) is False
    assert f([None]) is False


def test_join_upper():
    f = get_attr(load_solution(), "join_upper")
    assert f(["a", "b"]) == "A-B"
    assert f(["hey"]) == "HEY"
    assert f([]) == ""
    with pytest.raises(TypeError):
        f(["a", 2])


def test_describe_narrows_each_branch():
    f = get_attr(load_solution(), "describe")
    assert f(7) == "number 7"
    assert f("hi") == "text hi"
    assert f([1, 2]) == "list of 2 items"
    assert f([]) == "list of 0 items"


# ---- typing -----------------------------------------------------------------

def test_mypy_clean_on_module():
    proc = _mypy(workspace() / "solution.py", "--disallow-untyped-defs")
    assert proc.returncode == 0, (
        "mypy is not clean under --disallow-untyped-defs:\n" + proc.stdout + proc.stderr
    )


def test_mypy_narrowing_happens():
    snippet = workspace() / "_check_narrow.py"
    snippet.write_text(
        "from typing import assert_type\n"
        "from solution import is_str_list\n"
        "\n"
        "def check(v: list[object]) -> None:\n"
        "    if is_str_list(v):\n"
        "        assert_type(v, list[str])\n"
    )
    proc = _mypy(snippet)
    assert proc.returncode == 0, (
        "mypy did not narrow list[object] to list[str] — is is_str_list's "
        "return annotated TypeGuard[list[str]] (or TypeIs)?\n"
        + proc.stdout + proc.stderr
    )
