import pytest

from pytrain_grader import load_solution, get_attr


def retry():
    return get_attr(load_solution(), "retry")


def make_flaky(fail_times, exc=ValueError):
    calls = []

    def flaky(value="ok"):
        calls.append(1)
        if len(calls) <= fail_times:
            raise exc(f"failure {len(calls)}")
        return value

    return flaky, calls


def test_success_first_try_no_extra_attempts():
    r = retry()
    flaky, calls = make_flaky(0)
    wrapped = r(3)(flaky)
    assert wrapped("done") == "done"
    assert len(calls) == 1


def test_retries_until_success():
    r = retry()
    flaky, calls = make_flaky(2)
    wrapped = r(3)(flaky)
    assert wrapped() == "ok"
    assert len(calls) == 3


def test_raises_after_exhausting_attempts():
    r = retry()
    flaky, calls = make_flaky(5)
    wrapped = r(3)(flaky)
    with pytest.raises(ValueError, match="failure 3"):
        wrapped()
    assert len(calls) == 3


def test_times_one_means_single_attempt():
    r = retry()
    flaky, calls = make_flaky(1)
    wrapped = r(1)(flaky)
    with pytest.raises(ValueError):
        wrapped()
    assert len(calls) == 1


def test_unlisted_exception_propagates_immediately():
    r = retry()
    flaky, calls = make_flaky(2, exc=KeyError)
    wrapped = r(5)(flaky)  # only retries ValueError by default
    with pytest.raises(KeyError):
        wrapped()
    assert len(calls) == 1, "a non-listed exception must not be retried"


def test_custom_exception_tuple():
    r = retry()
    flaky, calls = make_flaky(2, exc=KeyError)
    wrapped = r(3, exceptions=(KeyError, OSError))(flaky)
    assert wrapped() == "ok"
    assert len(calls) == 3


def test_decorator_syntax_and_metadata():
    r = retry()

    @r(2)
    def fetch(x):
        """Fetch."""
        return x * 2

    assert fetch(21) == 42
    assert fetch.__name__ == "fetch"


def test_invalid_times_rejected_at_decoration_time():
    r = retry()
    with pytest.raises(ValueError):
        r(0)
    with pytest.raises(ValueError):
        r(-2)


def test_args_kwargs_passthrough():
    r = retry()

    @r(2)
    def combine(a, b, *, sep="-"):
        return f"{a}{sep}{b}"

    assert combine(1, 2) == "1-2"
    assert combine("x", "y", sep="+") == "x+y"
