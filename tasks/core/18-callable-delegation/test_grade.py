from types import SimpleNamespace

import pytest

from pytrain_grader import load_solution, get_attr


def classes():
    mod = load_solution()
    return get_attr(mod, "RunningMean"), get_attr(mod, "LoggingProxy")


# ---- RunningMean ------------------------------------------------------

def test_instances_are_callable():
    RunningMean, _ = classes()
    rm = RunningMean()
    assert callable(rm)


def test_running_mean_values():
    RunningMean, _ = classes()
    rm = RunningMean()
    assert rm(10) == pytest.approx(10.0)
    assert rm(20) == pytest.approx(15.0)
    assert rm(0) == pytest.approx(10.0)


def test_mean_is_true_division_float():
    RunningMean, _ = classes()
    rm = RunningMean()
    rm(1)
    out = rm(2)
    assert isinstance(out, float)
    assert out == pytest.approx(1.5)


def test_count_tracks_calls():
    RunningMean, _ = classes()
    rm = RunningMean()
    assert rm.count == 0
    rm(5)
    rm(7)
    rm(9)
    assert rm.count == 3


def test_instances_are_independent():
    RunningMean, _ = classes()
    a, b = RunningMean(), RunningMean()
    a(100)
    assert b(2) == pytest.approx(2.0)
    assert (a.count, b.count) == (1, 1)


# ---- LoggingProxy -----------------------------------------------------

def test_delegates_methods_bound_to_the_target():
    _, LoggingProxy = classes()
    items = [1, 2]
    p = LoggingProxy(items)
    p.append(3)
    assert items == [1, 2, 3]


def test_delegates_plain_values():
    _, LoggingProxy = classes()
    p = LoggingProxy(SimpleNamespace(colour="red", size=4))
    assert p.colour == "red"
    assert p.size == 4


def test_accessed_records_names_in_order_with_duplicates():
    _, LoggingProxy = classes()
    p = LoggingProxy(SimpleNamespace(colour="red", size=4))
    p.colour
    p.size
    p.colour
    assert p.accessed == ["colour", "size", "colour"]


def test_reading_accessed_is_not_recorded():
    _, LoggingProxy = classes()
    p = LoggingProxy(SimpleNamespace(x=1))
    assert p.accessed == []
    p.x
    log = p.accessed
    log2 = p.accessed
    assert log2 == ["x"]
    assert "accessed" not in log2


def test_missing_attribute_raises_attributeerror():
    _, LoggingProxy = classes()
    p = LoggingProxy(SimpleNamespace(x=1))
    with pytest.raises(AttributeError):
        p.definitely_not_there


def test_proxies_are_independent():
    _, LoggingProxy = classes()
    a = LoggingProxy(SimpleNamespace(x=1))
    b = LoggingProxy(SimpleNamespace(y=2))
    a.x
    assert a.accessed == ["x"]
    assert b.accessed == []
