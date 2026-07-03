import collections.abc
import inspect
import typing

import pytest

from pytrain_grader import load_solution, get_attr


# ---- apply_twice --------------------------------------------------------------

def test_apply_twice_behaviour():
    f = get_attr(load_solution(), "apply_twice")
    assert f(lambda x: x + 3, 10) == 16
    assert f(lambda x: x * 2, 1) == 4


def test_apply_twice_annotated_with_callable():
    f = get_attr(load_solution(), "apply_twice")
    hints = typing.get_type_hints(f)
    first = next(iter(inspect.signature(f).parameters))
    hint = hints.get(first)
    assert hint is not None, "apply_twice's fn parameter needs an annotation"
    assert typing.get_origin(hint) is collections.abc.Callable, (
        f"fn should be annotated Callable[[int], int], got {hint!r}"
    )


# ---- retry: behaviour ----------------------------------------------------------

def test_retry_succeeds_after_failures():
    retry = get_attr(load_solution(), "retry")
    attempts = []

    @retry(3)
    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise OSError("boom")
        return "ok"

    assert flaky() == "ok"
    assert len(attempts) == 3


def test_retry_gives_up_and_raises_last_exception():
    retry = get_attr(load_solution(), "retry")
    attempts = []

    @retry(2)
    def always_bad():
        attempts.append(1)
        raise ValueError(f"attempt {len(attempts)}")

    with pytest.raises(ValueError, match="attempt 2"):
        always_bad()
    assert len(attempts) == 2


def test_retry_first_try_success_calls_once():
    retry = get_attr(load_solution(), "retry")
    calls = []

    @retry(5)
    def fine(x):
        calls.append(x)
        return x + 1

    assert fine(41) == 42
    assert calls == [41]


def test_retry_forwards_args_and_kwargs():
    retry = get_attr(load_solution(), "retry")

    @retry(1)
    def combine(a, b, *, sep="-"):
        return f"{a}{sep}{b}"

    assert combine("x", "y") == "x-y"
    assert combine("x", "y", sep="+") == "x+y"


def test_retry_preserves_metadata():
    retry = get_attr(load_solution(), "retry")

    @retry(2)
    def documented():
        """docs live here"""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "docs live here"


# ---- retry: ParamSpec ----------------------------------------------------------

def test_a_paramspec_is_used():
    mod = load_solution()
    retry = get_attr(mod, "retry")
    module_level = any(isinstance(v, typing.ParamSpec) for v in vars(mod).values())
    pep695 = any(isinstance(tp, typing.ParamSpec)
                 for tp in getattr(retry, "__type_params__", ()))
    assert module_level or pep695, (
        "retry must be typed with a ParamSpec — declare P = ParamSpec('P') "
        "(or use PEP 695 `def retry[**P, R](...)`)"
    )


def test_retry_return_annotation_is_callable():
    retry = get_attr(load_solution(), "retry")
    hints = typing.get_type_hints(retry)
    ret = hints.get("return")
    assert ret is not None, "retry needs a return annotation"
    assert typing.get_origin(ret) is collections.abc.Callable, (
        f"retry should return Callable[[Callable[P, R]], Callable[P, R]], got {ret!r}"
    )
