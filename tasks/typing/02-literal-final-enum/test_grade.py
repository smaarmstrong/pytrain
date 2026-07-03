import enum
import inspect
import typing

import pytest

from pytrain_grader import load_solution, get_attr


def test_max_retries_value_and_final_annotation():
    mod = load_solution()
    assert getattr(mod, "MAX_RETRIES", None) == 3, "MAX_RETRIES must exist and equal 3"
    hints = typing.get_type_hints(mod)
    assert "MAX_RETRIES" in hints, "MAX_RETRIES needs a type annotation"
    hint = hints["MAX_RETRIES"]
    assert typing.get_origin(hint) is typing.Final and typing.get_args(hint) == (int,), (
        f"MAX_RETRIES should be annotated Final[int], got {hint!r}"
    )


def test_status_enum_members():
    Status = get_attr(load_solution(), "Status")
    assert issubclass(Status, enum.Enum), "Status must be an enum.Enum subclass"
    assert {m.name for m in Status} == {"OK", "WARN", "ERROR"}
    assert Status.OK.value == "ok"
    assert Status.WARN.value == "warn"
    assert Status.ERROR.value == "error"


def test_set_mode_behaviour():
    f = get_attr(load_solution(), "set_mode")
    assert f("r") == "mode set to r"
    assert f("w") == "mode set to w"
    assert f("a") == "mode set to a"
    with pytest.raises(ValueError):
        f("x")
    with pytest.raises(ValueError):
        f("")


def test_set_mode_literal_annotation():
    f = get_attr(load_solution(), "set_mode")
    hints = typing.get_type_hints(f)
    first = next(iter(inspect.signature(f).parameters))
    assert first in hints, "set_mode's parameter needs an annotation"
    hint = hints[first]
    assert typing.get_origin(hint) is typing.Literal, (
        f"set_mode's parameter should be a Literal, got {hint!r}"
    )
    assert set(typing.get_args(hint)) == {"r", "w", "a"}
    assert hints.get("return") is str


def test_severity_behaviour_and_enum_annotation():
    mod = load_solution()
    Status = get_attr(mod, "Status")
    f = get_attr(mod, "severity")
    assert f(Status.OK) == 0
    assert f(Status.WARN) == 1
    assert f(Status.ERROR) == 2
    hints = typing.get_type_hints(f)
    first = next(iter(inspect.signature(f).parameters))
    assert hints.get(first) is Status, (
        "severity's parameter must be annotated with your Status enum"
    )
    assert hints.get("return") is int
