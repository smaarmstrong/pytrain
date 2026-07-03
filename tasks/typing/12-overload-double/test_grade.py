import inspect
import typing

from pytrain_grader import load_solution, get_attr


# ---- behaviour --------------------------------------------------------------

def test_double_int():
    f = get_attr(load_solution(), "double")
    assert f(3) == 6
    assert f(0) == 0
    assert f(-2) == -4


def test_double_str():
    f = get_attr(load_solution(), "double")
    assert f("ab") == "abab"
    assert f("") == ""


def test_double_list_elementwise_new_list():
    f = get_attr(load_solution(), "double")
    src = [1, 2]
    out = f(src)
    assert out == [2, 4], "lists must be doubled ELEMENT-WISE"
    assert src == [1, 2], "the input list must not be mutated"
    assert out is not src
    assert f([]) == []


# ---- overload registry -------------------------------------------------------

def _overload_pairings(fn):
    """{param_type: return_type} for each registered overload."""
    pairs = {}
    for ov in typing.get_overloads(fn):
        hints = typing.get_type_hints(ov)
        ret = hints.pop("return", None)
        param_name = next(iter(inspect.signature(ov).parameters))
        pairs[hints.get(param_name)] = ret
    return pairs


def test_three_overloads_registered():
    f = get_attr(load_solution(), "double")
    ovs = typing.get_overloads(f)
    assert len(ovs) >= 3, (
        f"expected 3 @typing.overload declarations for double, "
        f"found {len(ovs)} — decorate the stubs with @overload"
    )


def test_overloads_pair_input_and_return_types():
    f = get_attr(load_solution(), "double")
    pairs = _overload_pairings(f)
    assert pairs.get(int) is int, "overload for int must return int"
    assert pairs.get(str) is str, "overload for str must return str"
    assert pairs.get(list[int]) == list[int], (
        "overload for list[int] must return list[int]"
    )
