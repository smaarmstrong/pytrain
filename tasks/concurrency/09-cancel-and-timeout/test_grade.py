import asyncio
import time

from pytrain_grader import load_solution, get_attr


def test_run_with_timeout_fast_coro_done():
    f = get_attr(load_solution(), "run_with_timeout")

    async def quick():
        await asyncio.sleep(0.05)
        return "payload"

    assert asyncio.run(f(quick(), 2.0)) == ("done", "payload")


def test_run_with_timeout_none_result_still_done():
    f = get_attr(load_solution(), "run_with_timeout")

    async def quick_none():
        await asyncio.sleep(0.01)

    assert asyncio.run(f(quick_none(), 2.0)) == ("done", None)


def test_run_with_timeout_times_out_promptly_and_cancels():
    f = get_attr(load_solution(), "run_with_timeout")
    state = {"cancelled": False, "finished": False}

    async def glacial():
        try:
            await asyncio.sleep(5)
            state["finished"] = True
            return "too late"
        except asyncio.CancelledError:
            state["cancelled"] = True
            raise

    start = time.monotonic()
    out = asyncio.run(f(glacial(), 0.2))
    elapsed = time.monotonic() - start
    assert out == ("timeout", None)
    assert elapsed < 2.0, f"timeout of 0.2s took {elapsed:.2f}s to trigger"
    assert state["cancelled"] and not state["finished"], (
        "the slow coroutine must be cancelled on timeout"
    )


def test_cancel_after_kills_a_long_task():
    f = get_attr(load_solution(), "cancel_after")
    state = {"cancelled": False, "finished": False}

    async def glacial():
        try:
            await asyncio.sleep(5)
            state["finished"] = True
            return "too late"
        except asyncio.CancelledError:
            state["cancelled"] = True
            raise

    start = time.monotonic()
    out = asyncio.run(f(glacial, 0.1))
    elapsed = time.monotonic() - start
    assert out == ("cancelled", None)
    assert elapsed < 2.0, f"cancelling after 0.1s took {elapsed:.2f}s"
    assert state["cancelled"] and not state["finished"], (
        "the task's CancelledError cleanup never ran — cancel() the task "
        "and then await it"
    )


def test_cancel_after_lets_a_quick_task_finish():
    f = get_attr(load_solution(), "cancel_after")
    state = {"cancelled": False}

    async def quick():
        try:
            await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            state["cancelled"] = True
            raise
        return "made it"

    out = asyncio.run(f(quick, 0.5))
    assert out == ("finished", "made it")
    assert not state["cancelled"], "the quick task should not have been cancelled"


def test_cancel_after_uses_a_real_task():
    # create_task means the worker starts making progress DURING the delay,
    # not after it: observable because it records a tick before the cancel.
    f = get_attr(load_solution(), "cancel_after")
    ticks = []

    async def worker():
        ticks.append("started")
        await asyncio.sleep(5)
        return "never"

    out = asyncio.run(f(worker, 0.1))
    assert out == ("cancelled", None)
    assert ticks == ["started"], (
        "the worker never started running before the cancel — schedule it "
        "with asyncio.create_task, then sleep"
    )
