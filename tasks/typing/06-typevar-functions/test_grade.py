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

def test_first():
    f = get_attr(load_solution(), "first")
    assert f([10, 20]) == 10
    assert f((5,)) == 5
    assert f("hello") == "h"
    with pytest.raises(ValueError):
        f([])
    with pytest.raises(ValueError):
        f(())


def test_pairs_stops_at_shorter():
    f = get_attr(load_solution(), "pairs")
    assert f([1, 2, 3], ["x", "y"]) == [(1, "x"), (2, "y")]
    assert f([], ["x"]) == []
    assert f(iter([1, 2]), iter("ab")) == [(1, "a"), (2, "b")]


def test_dedupe_keeps_first_occurrence():
    f = get_attr(load_solution(), "dedupe")
    assert f("abcabc") == ["a", "b", "c"]
    assert f([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert f([]) == []
    assert f(iter([1, 1, 1])) == [1]


# ---- typing -----------------------------------------------------------------

def test_mypy_clean_on_module():
    proc = _mypy(workspace() / "solution.py", "--disallow-untyped-defs")
    assert proc.returncode == 0, (
        "mypy is not clean under --disallow-untyped-defs:\n" + proc.stdout + proc.stderr
    )


def test_mypy_generics_propagate():
    snippet = workspace() / "_check_generics.py"
    snippet.write_text(
        "from typing import assert_type\n"
        "from solution import first, pairs, dedupe\n"
        "\n"
        "assert_type(first([1, 2, 3]), int)\n"
        'assert_type(first(("a", "b")), str)\n'
        'assert_type(pairs([1, 2], ["x"]), list[tuple[int, str]])\n'
        'assert_type(dedupe(["a", "b", "a"]), list[str])\n'
    )
    proc = _mypy(snippet)
    assert proc.returncode == 0, (
        "the generic types don't propagate (mypy assert_type failed — did a "
        "function return Any or a non-generic type?):\n" + proc.stdout + proc.stderr
    )
