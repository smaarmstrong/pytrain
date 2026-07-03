import pytest

from pytrain_grader import load_solution, get_attr


def rollback_cls():
    return get_attr(load_solution(), "Rollback")


def test_enter_returns_the_same_dict():
    Rollback = rollback_cls()
    d = {"a": 1}
    with Rollback(d) as d2:
        assert d2 is d


def test_clean_exit_keeps_changes():
    Rollback = rollback_cls()
    d = {"a": 1}
    with Rollback(d) as d2:
        d2["b"] = 2
        d2["a"] = 10
    assert d == {"a": 10, "b": 2}


def test_exception_rolls_back_added_and_changed():
    Rollback = rollback_cls()
    d = {"a": 1}
    with pytest.raises(RuntimeError, match="boom"):
        with Rollback(d):
            d["a"] = 99
            d["junk"] = True
            raise RuntimeError("boom")
    assert d == {"a": 1}


def test_exception_reinstates_deleted_keys():
    Rollback = rollback_cls()
    d = {"a": 1, "b": 2}
    with pytest.raises(ValueError):
        with Rollback(d):
            del d["b"]
            raise ValueError()
    assert d == {"a": 1, "b": 2}


def test_default_propagates_the_original_exception():
    Rollback = rollback_cls()
    d = {}

    class Custom(Exception):
        pass

    with pytest.raises(Custom):
        with Rollback(d):
            raise Custom("mine")


def test_swallow_true_suppresses_but_still_rolls_back():
    Rollback = rollback_cls()
    d = {"a": 1}
    reached = False
    with Rollback(d, swallow=True):
        d["a"] = 2
        raise ValueError("ignored")
    reached = True  # only reachable if the exception was swallowed
    assert reached
    assert d == {"a": 1}


def test_swallow_true_clean_exit_still_keeps_changes():
    Rollback = rollback_cls()
    d = {}
    with Rollback(d, swallow=True):
        d["x"] = 1
    assert d == {"x": 1}


def test_instance_reusable_with_fresh_snapshot():
    Rollback = rollback_cls()
    d = {"n": 0}
    rb = Rollback(d)
    with rb:
        d["n"] = 1  # kept
    with pytest.raises(RuntimeError):
        with rb:
            d["n"] = 2
            raise RuntimeError()
    assert d == {"n": 1}, "second entry must snapshot the post-first-block state"
