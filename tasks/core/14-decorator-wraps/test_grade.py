import pytest

from pytrain_grader import load_solution, get_attr


def decorator():
    return get_attr(load_solution(), "count_calls")


def sample(a, b=10):
    """Add things."""
    return a + b


def test_passthrough_args_kwargs_and_return():
    dec = decorator()
    wrapped = dec(sample)
    assert wrapped(1) == 11
    assert wrapped(1, 2) == 3
    assert wrapped(1, b=5) == 6


def test_calls_counter():
    dec = decorator()
    wrapped = dec(sample)
    assert wrapped.calls == 0
    wrapped(1)
    wrapped(2, b=0)
    assert wrapped.calls == 2


def test_counts_raising_calls_and_propagates():
    dec = decorator()

    def boom():
        raise RuntimeError("nope")

    wrapped = dec(boom)
    with pytest.raises(RuntimeError, match="nope"):
        wrapped()
    assert wrapped.calls == 1


def test_metadata_preserved():
    dec = decorator()
    wrapped = dec(sample)
    assert wrapped.__name__ == "sample"
    assert wrapped.__doc__ == "Add things."


def test_dunder_wrapped_is_original():
    dec = decorator()
    wrapped = dec(sample)
    assert wrapped.__wrapped__ is sample
    assert wrapped.__wrapped__(1, 1) == 2


def test_independent_counters():
    dec = decorator()
    w1 = dec(sample)
    w2 = dec(sample)
    w1(1)
    w1(2)
    w2(3)
    assert w1.calls == 2
    assert w2.calls == 1


def test_works_as_decorator_syntax():
    dec = decorator()

    @dec
    def double(x):
        """Twice."""
        return 2 * x

    assert double(4) == 8
    assert double.calls == 1
    assert double.__name__ == "double"
