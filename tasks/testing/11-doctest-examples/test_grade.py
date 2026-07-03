"""Grader: runs the learner's doctests via the doctest module (all must pass,
with at least two per function actually invoking it) and re-checks that the
functions still behave as specified."""
import doctest

import pytest

from pytrain_grader import get_attr, load_solution

REQUIRED = ("c_to_f", "clamp", "initials")


def _doctests(mod):
    return doctest.DocTestFinder(exclude_empty=False).find(mod)


def test_each_function_has_two_examples_calling_it():
    mod = load_solution()
    tests = _doctests(mod)
    for fn in REQUIRED:
        get_attr(mod, fn)
        examples = []
        for t in tests:
            if t.name.endswith("." + fn):
                examples.extend(t.examples)
        calling = [ex for ex in examples if fn in ex.source]
        assert len(calling) >= 2, (
            f"the docstring of {fn} needs at least two `>>> {fn}(...)` examples "
            f"(found {len(calling)} that call it)"
        )


def test_all_doctests_pass():
    mod = load_solution()
    runner = doctest.DocTestRunner(verbose=False)
    attempted = failed = 0
    for t in _doctests(mod):
        result = runner.run(t)
        attempted += result.attempted
        failed += result.failed
    assert attempted >= 6, (
        f"expected at least six doctest examples across the module, found {attempted}"
    )
    assert failed == 0, (
        f"{failed} doctest example(s) fail — run `python -m doctest solution.py -v`"
    )


def test_c_to_f_behaviour_unchanged():
    f = get_attr(load_solution(), "c_to_f")
    assert f(0) == 32.0
    assert f(100) == 212.0
    assert f(-40) == -40.0


def test_clamp_behaviour_unchanged():
    clamp = get_attr(load_solution(), "clamp")
    assert clamp(5, 0, 10) == 5
    assert clamp(-3, 0, 10) == 0
    assert clamp(99, 0, 10) == 10
    with pytest.raises(ValueError):
        clamp(1, 5, 0)


def test_initials_behaviour_unchanged():
    initials = get_attr(load_solution(), "initials")
    assert initials("ada lovelace") == "A.L."
    assert initials("grace brewster murray hopper") == "G.B.M.H."
    assert initials("plato") == "P."
    assert initials("") == ""
