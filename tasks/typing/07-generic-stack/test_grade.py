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

def test_lifo_order():
    Stack = get_attr(load_solution(), "Stack")
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert [s.pop(), s.pop(), s.pop()] == [3, 2, 1]


def test_peek_does_not_remove():
    Stack = get_attr(load_solution(), "Stack")
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.peek() == "b"
    assert s.peek() == "b"
    assert len(s) == 2


def test_len_and_is_empty():
    Stack = get_attr(load_solution(), "Stack")
    s = Stack()
    assert s.is_empty() is True
    assert len(s) == 0
    s.push(42)
    assert s.is_empty() is False
    assert len(s) == 1
    s.pop()
    assert s.is_empty() is True


def test_empty_pop_and_peek_raise_indexerror():
    Stack = get_attr(load_solution(), "Stack")
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()


def test_subscriptable_at_runtime():
    Stack = get_attr(load_solution(), "Stack")
    try:
        parametrized = Stack[int]
    except TypeError:
        pytest.fail("Stack[int] raised TypeError — is Stack generic?")
    s = parametrized()
    s.push(1)
    assert s.pop() == 1


# ---- typing -----------------------------------------------------------------

def test_mypy_clean_on_module():
    proc = _mypy(workspace() / "solution.py", "--disallow-untyped-defs")
    assert proc.returncode == 0, (
        "mypy is not clean under --disallow-untyped-defs:\n" + proc.stdout + proc.stderr
    )


def test_mypy_element_type_propagates():
    snippet = workspace() / "_check_stack_ok.py"
    snippet.write_text(
        "from typing import assert_type\n"
        "from solution import Stack\n"
        "\n"
        "s: Stack[int] = Stack()\n"
        "s.push(1)\n"
        "s.push(2)\n"
        "assert_type(s.pop(), int)\n"
        "assert_type(s.peek(), int)\n"
        "assert_type(len(s), int)\n"
        "t: Stack[str] = Stack()\n"
        't.push("a")\n'
        "assert_type(t.pop(), str)\n"
    )
    proc = _mypy(snippet)
    assert proc.returncode == 0, (
        "Stack's element type doesn't propagate through push/pop/peek:\n"
        + proc.stdout + proc.stderr
    )


def test_mypy_rejects_wrong_element_type():
    snippet = workspace() / "_check_stack_bad.py"
    snippet.write_text(
        "from solution import Stack\n"
        "\n"
        "s: Stack[int] = Stack()\n"
        's.push("oops")\n'
    )
    proc = _mypy(snippet)
    assert proc.returncode != 0, (
        "mypy accepted pushing a str onto Stack[int] — is push annotated with "
        "the type variable?"
    )
