from types import SimpleNamespace

import pytest

from pytrain_grader import load_solution, get_attr


def funcs():
    mod = load_solution()
    return get_attr(mod, "patched"), get_attr(mod, "suppress_and_log")


# ---- patched ----------------------------------------------------------

def test_patched_sets_value_inside_and_yields_the_object():
    patched, _ = funcs()
    cfg = SimpleNamespace(retries=3)
    with patched(cfg, "retries", 10) as got:
        assert got is cfg
        assert cfg.retries == 10


def test_patched_restores_previous_value_on_clean_exit():
    patched, _ = funcs()
    cfg = SimpleNamespace(retries=3)
    with patched(cfg, "retries", 10):
        pass
    assert cfg.retries == 3


def test_patched_restores_on_exception_and_propagates():
    patched, _ = funcs()
    cfg = SimpleNamespace(mode="safe")
    with pytest.raises(RuntimeError, match="boom"):
        with patched(cfg, "mode", "fast"):
            assert cfg.mode == "fast"
            raise RuntimeError("boom")
    assert cfg.mode == "safe"


def test_patched_removes_attribute_that_did_not_exist():
    patched, _ = funcs()
    cfg = SimpleNamespace()
    with patched(cfg, "debug", True):
        assert cfg.debug is True
    assert not hasattr(cfg, "debug")


def test_patched_removes_missing_attribute_even_on_exception():
    patched, _ = funcs()
    cfg = SimpleNamespace()
    with pytest.raises(ValueError):
        with patched(cfg, "debug", True):
            raise ValueError()
    assert not hasattr(cfg, "debug")


def test_patched_each_call_is_independent():
    patched, _ = funcs()
    a = SimpleNamespace(x=1)
    b = SimpleNamespace(x=2)
    with patched(a, "x", 10):
        with patched(b, "x", 20):
            assert (a.x, b.x) == (10, 20)
        assert (a.x, b.x) == (10, 2)
    assert (a.x, b.x) == (1, 2)


# ---- suppress_and_log -------------------------------------------------

def test_suppresses_listed_type_and_logs_the_exception_object():
    _, sal = funcs()
    log = []
    reached = False
    with sal(log, ValueError):
        raise ValueError("bad input")
    reached = True
    assert reached
    assert len(log) == 1
    assert isinstance(log[0], ValueError)
    assert str(log[0]) == "bad input"


def test_subclasses_are_suppressed_like_except():
    _, sal = funcs()

    class AppError(Exception):
        pass

    class DiskError(AppError):
        pass

    log = []
    with sal(log, AppError):
        raise DiskError("disk full")
    assert len(log) == 1 and isinstance(log[0], DiskError)


def test_unlisted_exception_propagates_and_logs_nothing():
    _, sal = funcs()
    log = []
    with pytest.raises(KeyError):
        with sal(log, ValueError, TypeError):
            raise KeyError("nope")
    assert log == []


def test_multiple_types_all_suppressed():
    _, sal = funcs()
    log = []
    with sal(log, ValueError, TypeError):
        raise TypeError("t")
    with sal(log, ValueError, TypeError):
        raise ValueError("v")
    assert [type(e) for e in log] == [TypeError, ValueError]


def test_clean_exit_logs_nothing():
    _, sal = funcs()
    log = []
    with sal(log, Exception):
        x = 1 + 1
    assert x == 2
    assert log == []
