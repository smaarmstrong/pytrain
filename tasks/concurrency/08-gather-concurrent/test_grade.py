import asyncio
import time

from pytrain_grader import load_solution, get_attr


async def _echo(delay, value):
    await asyncio.sleep(delay)
    return value


def test_results_in_input_order_not_completion_order():
    fan_out = get_attr(load_solution(), "fan_out")
    # the first job is the SLOWEST — input order must still win
    out = asyncio.run(fan_out(_echo, [(0.3, "a"), (0.05, "b"), (0.15, "c")]))
    assert out == ["a", "b", "c"]


def test_empty_args_list():
    fan_out = get_attr(load_solution(), "fan_out")
    assert asyncio.run(fan_out(_echo, [])) == []


def test_single_job():
    fan_out = get_attr(load_solution(), "fan_out")
    assert asyncio.run(fan_out(_echo, [(0.01, 99)])) == [99]


def test_gather_overlaps_the_sleeps():
    fan_out = get_attr(load_solution(), "fan_out")
    start = time.monotonic()
    out = asyncio.run(fan_out(_echo, [(0.3, i) for i in range(5)]))
    elapsed = time.monotonic() - start
    assert out == [0, 1, 2, 3, 4]
    # concurrent ~0.3s; sequential would be 1.5s
    assert elapsed < 1.0, (
        f"5 x 0.3s workers took {elapsed:.2f}s — that's sequential awaiting, "
        "use asyncio.gather"
    )


def test_timed_fan_out_reports_elapsed():
    timed_fan_out = get_attr(load_solution(), "timed_fan_out")
    start = time.monotonic()
    results, reported = asyncio.run(
        timed_fan_out(_echo, [(0.2, "p"), (0.2, "q"), (0.2, "r")])
    )
    actual = time.monotonic() - start
    assert results == ["p", "q", "r"]
    assert isinstance(reported, float)
    # reported time covers the gather (>= one sleep) and never exceeds
    # what we measured from outside
    assert 0.15 <= reported <= actual + 0.05, (
        f"reported {reported:.2f}s but the whole call took {actual:.2f}s"
    )
    assert actual < 1.0, "timed_fan_out must still run workers concurrently"
