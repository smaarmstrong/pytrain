import asyncio
import time
from collections import Counter

from pytrain_grader import load_solution, get_attr


def _run_pipeline():
    return get_attr(load_solution(), "run_pipeline")


async def _double(x):
    await asyncio.sleep(0.001)
    return x * 2


def test_every_item_processed_once():
    run_pipeline = _run_pipeline()
    out = asyncio.run(run_pipeline([1, 2, 3, 4, 5], _double, 2))
    assert Counter(out) == Counter([2, 4, 6, 8, 10])


def test_single_consumer_and_duplicates():
    run_pipeline = _run_pipeline()
    out = asyncio.run(run_pipeline([3, 3, 3], _double, 1))
    assert Counter(out) == Counter([6, 6, 6])


def test_empty_items():
    run_pipeline = _run_pipeline()
    assert asyncio.run(run_pipeline([], _double, 4)) == []


def test_more_consumers_than_items():
    run_pipeline = _run_pipeline()
    out = asyncio.run(run_pipeline([10], _double, 8))
    assert out == [20]


def test_consumers_overlap_the_waits():
    run_pipeline = _run_pipeline()

    async def slow(x):
        await asyncio.sleep(0.2)
        return x

    start = time.monotonic()
    out = asyncio.run(run_pipeline(list(range(8)), slow, 4))
    elapsed = time.monotonic() - start
    assert Counter(out) == Counter(range(8))
    # 4 consumers x 2 rounds of 0.2s: ideal ~0.4s; sequential = 1.6s
    assert elapsed < 1.2, (
        f"8 x 0.2s jobs with 4 consumers took {elapsed:.2f}s — consumers "
        "are not running concurrently"
    )


def test_no_consumer_tasks_left_running():
    run_pipeline = _run_pipeline()

    async def scenario():
        before = set(asyncio.all_tasks())
        result = await run_pipeline([1, 2, 3], _double, 3)
        # let any about-to-exit tasks finish their final step
        await asyncio.sleep(0.05)
        leftovers = [
            t for t in asyncio.all_tasks() - before
            if not t.done() and t is not asyncio.current_task()
        ]
        return result, leftovers

    result, leftovers = asyncio.run(scenario())
    assert Counter(result) == Counter([2, 4, 6])
    assert not leftovers, (
        f"{len(leftovers)} consumer task(s) still alive after run_pipeline "
        "returned — shut them down (sentinels or join+cancel)"
    )
