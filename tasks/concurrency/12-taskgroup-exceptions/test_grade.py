import asyncio
import time

import pytest

from pytrain_grader import load_solution, get_attr


async def _echo(delay, value):
    await asyncio.sleep(delay)
    return value


def _leaves(exc):
    """Flatten (possibly nested) ExceptionGroups to leaf exceptions."""
    if isinstance(exc, BaseExceptionGroup):
        out = []
        for sub in exc.exceptions:
            out.extend(_leaves(sub))
        return out
    return [exc]


def test_run_all_success_ordered():
    run_all = get_attr(load_solution(), "run_all")
    out = asyncio.run(run_all([_echo(0.05, "a"), (_echo(0.01, "b")), _echo(0.03, "c")]))
    assert out == ["a", "b", "c"]


def test_run_all_empty():
    run_all = get_attr(load_solution(), "run_all")
    assert asyncio.run(run_all([])) == []


def test_run_all_failure_raises_group_and_cancels_siblings():
    run_all = get_attr(load_solution(), "run_all")
    cancelled = []

    async def sleeper(tag):
        try:
            await asyncio.sleep(5)
            return tag
        except asyncio.CancelledError:
            cancelled.append(tag)
            raise

    async def boom():
        await asyncio.sleep(0.05)
        raise ValueError("boom")

    start = time.monotonic()
    with pytest.raises(BaseExceptionGroup) as excinfo:
        asyncio.run(run_all([sleeper("s1"), boom(), sleeper("s2")]))
    elapsed = time.monotonic() - start

    leaves = _leaves(excinfo.value)
    assert any(isinstance(e, ValueError) for e in leaves), (
        f"the ExceptionGroup must contain the original ValueError, got {leaves!r}"
    )
    assert elapsed < 2.0, (
        f"failure after 0.05s took {elapsed:.2f}s to surface — the group "
        "must cancel the 5s siblings, not wait for them"
    )
    assert sorted(cancelled) == ["s1", "s2"], (
        f"siblings not cancelled (cancelled={cancelled}) — run tasks INSIDE "
        "a TaskGroup so the first failure cancels the rest"
    )


def test_run_and_summarise_ok():
    f = get_attr(load_solution(), "run_and_summarise")
    status, results = asyncio.run(f([_echo(0.02, 1), _echo(0.01, 2)]))
    assert status == "ok"
    assert results == [1, 2]


def test_run_and_summarise_error_names():
    f = get_attr(load_solution(), "run_and_summarise")

    async def fail_with(exc):
        await asyncio.sleep(0)
        raise exc

    async def sleeper():
        await asyncio.sleep(5)

    status, names = asyncio.run(
        f([fail_with(ValueError("v")), fail_with(KeyError("k")), sleeper()])
    )
    assert status == "error"
    assert names == sorted(names), "type names must be sorted"
    # ValueError raised first is always in the group; KeyError may or may
    # not have raised before cancellation reached it.
    assert "ValueError" in names
    assert set(names) <= {"ValueError", "KeyError"}, f"unexpected names {names}"


def test_run_and_summarise_does_not_leak_the_group():
    f = get_attr(load_solution(), "run_and_summarise")

    async def instant_fail():
        await asyncio.sleep(0.01)
        raise RuntimeError("nope")

    # must not raise
    status, names = asyncio.run(f([instant_fail()]))
    assert status == "error"
    assert names == ["RuntimeError"]
