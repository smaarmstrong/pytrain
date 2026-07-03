import typing

import pytest

from pytrain_grader import load_solution, get_attr


# ---- behaviour --------------------------------------------------------------

def test_pick():
    f = get_attr(load_solution(), "pick")
    assert f(["a", "b", "c"], 1) == "b"
    assert f((10, 20), 0) == 10
    assert f("xyz", -1) == "z"
    with pytest.raises(IndexError):
        f([1], 5)


def test_swap():
    f = get_attr(load_solution(), "swap")
    assert f((1, "x")) == ("x", 1)
    assert f(("a", "b")) == ("b", "a")


def test_pair_behaviour():
    Pair = get_attr(load_solution(), "Pair")
    p = Pair(1, 2)
    assert (p.first, p.second) == (1, 2)
    assert p.as_tuple() == (1, 2)
    q = p.swapped()
    assert q.as_tuple() == (2, 1)
    assert p.as_tuple() == (1, 2), "swapped() must return a NEW Pair"


# ---- PEP 695 syntax ---------------------------------------------------------

def _type_params(obj, name):
    params = getattr(obj, "__type_params__", ())
    assert params, (
        f"{name} has no __type_params__ — declare its type parameters with "
        f"PEP 695 syntax ({name}[T](...)), not a module-level TypeVar"
    )
    return params


def test_pick_uses_pep695():
    params = _type_params(get_attr(load_solution(), "pick"), "pick")
    assert len(params) == 1
    assert all(isinstance(tp, typing.TypeVar) for tp in params)


def test_swap_uses_pep695_with_two_params():
    params = _type_params(get_attr(load_solution(), "swap"), "swap")
    assert len(params) == 2, "swap should declare two type parameters [A, B]"


def test_pair_class_uses_pep695():
    Pair = get_attr(load_solution(), "Pair")
    params = _type_params(Pair, "Pair")
    assert len(params) == 1
    # the new syntax also makes the class subscriptable
    Pair[int]
