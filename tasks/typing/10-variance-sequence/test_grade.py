import collections.abc
import inspect
import typing

from pytrain_grader import load_solution, get_attr


class WordSeq(collections.abc.Sequence):
    """A Sequence that is neither list nor tuple."""

    def __init__(self, *items):
        self._items = items

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]


# ---- Box: behaviour + covariance --------------------------------------------

def test_box_get():
    Box = get_attr(load_solution(), "Box")
    assert Box("hi").get() == "hi"
    assert Box(42).get() == 42
    assert Box(None).get() is None


def test_box_type_parameter_is_covariant():
    Box = get_attr(load_solution(), "Box")
    params = tuple(getattr(Box, "__type_params__", ()) or
                   getattr(Box, "__parameters__", ()))
    assert params, "Box must be generic (Generic[T_co] or class Box[T]:)"
    tv = params[0]
    assert tv.__covariant__ or getattr(tv, "__infer_variance__", False), (
        "Box's type variable must be covariant — TypeVar('T_co', covariant=True) "
        "(or a PEP 695 parameter, which infers variance)"
    )


def test_box_subscriptable_at_runtime():
    Box = get_attr(load_solution(), "Box")
    assert Box[int](3).get() == 3


# ---- Sequence-typed functions ------------------------------------------------

def _param_hint(fn):
    hints = typing.get_type_hints(fn)
    first = next(iter(inspect.signature(fn).parameters))
    return hints.get(first)


def test_total_works_on_any_sequence():
    f = get_attr(load_solution(), "total")
    assert f([1.0, 2.5]) == 3.5
    assert f((1, 2, 3)) == 6
    assert f(range(4)) == 6
    assert f(WordSeq(2, 4)) == 6
    assert f(()) == 0


def test_total_annotated_with_sequence_not_list():
    f = get_attr(load_solution(), "total")
    hint = _param_hint(f)
    assert hint is not None, "total's parameter needs an annotation"
    assert typing.get_origin(hint) is collections.abc.Sequence, (
        f"total's parameter should be Sequence[float], got {hint!r}"
    )


def test_labels_upper_works_on_any_sequence():
    f = get_attr(load_solution(), "labels_upper")
    assert f(("a", "b")) == ["A", "B"]
    assert f(["mix", "It"]) == ["MIX", "IT"]
    assert f(WordSeq("x", "y")) == ["X", "Y"]
    assert f([]) == []


def test_labels_upper_annotated_with_sequence_of_str():
    f = get_attr(load_solution(), "labels_upper")
    hint = _param_hint(f)
    assert hint is not None, "labels_upper's parameter needs an annotation"
    assert typing.get_origin(hint) is collections.abc.Sequence
    assert typing.get_args(hint) == (str,)
