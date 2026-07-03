import inspect
import subprocess
import sys
import types
import typing

from pytrain_grader import load_solution, get_attr, workspace


# ---- behaviour --------------------------------------------------------------

def test_parse_port_behaviour():
    f = get_attr(load_solution(), "parse_port")
    assert f("8080") == 8080
    assert f(" 443 ") == 443
    assert f("abc") is None
    assert f("70000") is None
    assert f("-1") is None
    assert f("0") == 0


def test_normalize_host_behaviour():
    f = get_attr(load_solution(), "normalize_host")
    assert f(None) == "localhost"
    assert f("   ") == "localhost"
    assert f(" EXAMPLE.com ") == "example.com"


def test_get_flag_behaviour():
    f = get_attr(load_solution(), "get_flag")
    assert f({"debug": "YES"}, "debug") is True
    assert f({"debug": "0"}, "debug", True) is False
    assert f({}, "debug") is False
    assert f({}, "debug", True) is True


def test_summarize_behaviour():
    f = get_attr(load_solution(), "summarize")
    assert f({"b": "2", "a": "1"}) == "a=1, b=2"
    assert f({}) == ""


# ---- typing -----------------------------------------------------------------

def _is_union_with_none(hint, inner):
    origin = typing.get_origin(hint)
    if origin not in (typing.Union, types.UnionType):
        return False
    return set(typing.get_args(hint)) == {inner, type(None)}


def _first_param_hint(fn):
    hints = typing.get_type_hints(fn)
    first = next(iter(inspect.signature(fn).parameters))
    if first not in hints:
        return None
    return hints[first]


def test_parse_port_returns_optional_int():
    f = get_attr(load_solution(), "parse_port")
    hints = typing.get_type_hints(f)
    assert "return" in hints, "parse_port needs a return annotation"
    assert _is_union_with_none(hints["return"], int), (
        f"parse_port should be annotated to return an int/None union, "
        f"got {hints['return']!r}"
    )


def test_normalize_host_accepts_optional_str():
    f = get_attr(load_solution(), "normalize_host")
    hint = _first_param_hint(f)
    assert hint is not None, "normalize_host's parameter needs an annotation"
    assert _is_union_with_none(hint, str), (
        f"normalize_host's parameter should be a str/None union, got {hint!r}"
    )
    assert typing.get_type_hints(f).get("return") is str


def test_mypy_clean():
    proc = subprocess.run(
        [sys.executable, "-m", "mypy", "--no-error-summary", "--soft-error-limit=-1",
         "--disallow-untyped-defs", "--disallow-incomplete-defs",
         str(workspace() / "solution.py")],
        capture_output=True, text=True, cwd=str(workspace()),
    )
    assert proc.returncode == 0, (
        "mypy is not clean under --disallow-untyped-defs --disallow-incomplete-defs:\n"
        + proc.stdout + proc.stderr
    )
