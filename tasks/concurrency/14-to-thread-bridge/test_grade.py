import asyncio
import threading
import time

from pytrain_grader import load_solution, get_attr


def _blocking_echo(x):
    time.sleep(0.3)  # deliberately time.sleep: BLOCKS whatever thread runs it
    return x


def test_fetch_one_returns_result():
    fetch_one = get_attr(load_solution(), "fetch_one")

    def lookup(key):
        time.sleep(0.05)
        return key.upper()

    assert asyncio.run(fetch_one(lookup, "abc")) == "ABC"


def test_fetch_one_runs_off_the_loop_thread():
    fetch_one = get_attr(load_solution(), "fetch_one")

    def where(_):
        return threading.get_ident()

    async def scenario():
        loop_thread = threading.get_ident()
        worker_thread = await fetch_one(where, None)
        return loop_thread, worker_thread

    loop_thread, worker_thread = asyncio.run(scenario())
    assert worker_thread != loop_thread, (
        "blocking_fn ran on the event-loop thread — bridge it with "
        "asyncio.to_thread / run_in_executor"
    )


def test_fetch_many_ordered_and_empty():
    fetch_many = get_attr(load_solution(), "fetch_many")

    def stamp(x):
        time.sleep(0.01)
        return x * 10

    assert asyncio.run(fetch_many(stamp, [3, 1, 2])) == [30, 10, 20]
    assert asyncio.run(fetch_many(stamp, [])) == []


def test_loop_keeps_beating_while_blocking_work_runs():
    fetch_many = get_attr(load_solution(), "fetch_many")

    async def scenario():
        ticks = []

        async def heartbeat():
            while True:
                await asyncio.sleep(0.05)
                ticks.append(time.monotonic())

        hb = asyncio.create_task(heartbeat())
        start = time.monotonic()
        results = await fetch_many(_blocking_echo, ["a", "b", "c", "d"])
        elapsed = time.monotonic() - start
        hb.cancel()
        try:
            await hb
        except asyncio.CancelledError:
            pass
        return results, elapsed, len(ticks)

    results, elapsed, n_ticks = asyncio.run(scenario())
    assert results == ["a", "b", "c", "d"]
    # concurrent-and-bridged ~0.3s; blocking the loop (or sequential
    # bridging) = 1.2s
    assert elapsed < 1.0, (
        f"4 x 0.3s blocking calls took {elapsed:.2f}s — they must run "
        "concurrently on worker threads"
    )
    # ~6 ticks expected during 0.3s+; a blocked loop produces none
    assert n_ticks >= 2, (
        f"the heartbeat only ticked {n_ticks} times — the event loop was "
        "blocked while blocking_fn ran"
    )
