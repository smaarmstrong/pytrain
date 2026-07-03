import asyncio
import time

from pytrain_grader import load_solution, get_attr


def test_fetch_value_is_a_coroutine_function():
    fetch_value = get_attr(load_solution(), "fetch_value")
    assert asyncio.iscoroutinefunction(fetch_value), (
        "fetch_value must be `async def`"
    )


def test_calling_does_not_run():
    fetch_value = get_attr(load_solution(), "fetch_value")
    start = time.monotonic()
    coro = fetch_value(5.0, "never awaited")  # a 5s sleep, if it ran
    elapsed = time.monotonic() - start
    assert asyncio.iscoroutine(coro)
    assert elapsed < 1.0, "calling a coroutine function must not execute it"
    coro.close()  # avoid the 'never awaited' warning


def test_fetch_value_returns_value():
    fetch_value = get_attr(load_solution(), "fetch_value")
    assert asyncio.run(fetch_value(0.01, 42)) == 42
    assert asyncio.run(fetch_value(0.01, None)) is None


def test_fetch_all_order_and_types():
    fetch_all = get_attr(load_solution(), "fetch_all")
    assert asyncio.iscoroutinefunction(fetch_all)
    out = asyncio.run(fetch_all([(0.01, "a"), (0.01, "b"), (0.01, "c")]))
    assert out == ["a", "b", "c"]
    assert asyncio.run(fetch_all([])) == []


def test_fetch_all_is_sequential():
    fetch_all = get_attr(load_solution(), "fetch_all")
    start = time.monotonic()
    out = asyncio.run(fetch_all([(0.1, 1), (0.1, 2), (0.1, 3)]))
    elapsed = time.monotonic() - start
    assert out == [1, 2, 3]
    # Three awaited-in-turn 0.1s sleeps can't finish faster than ~0.3s.
    assert elapsed >= 0.25, (
        f"finished in {elapsed:.2f}s — fetch_all must await one fetch at a "
        "time (concurrency is the NEXT task)"
    )


def test_main_runs_from_sync_code():
    main = get_attr(load_solution(), "main")
    assert not asyncio.iscoroutinefunction(main), (
        "main must be a plain def that uses asyncio.run internally"
    )
    assert main([(0.01, "x"), (0.01, "y")]) == ["x", "y"]
    assert main([]) == []
