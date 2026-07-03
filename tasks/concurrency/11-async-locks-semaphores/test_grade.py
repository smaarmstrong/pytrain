import asyncio

import pytest

from pytrain_grader import load_solution, get_attr


class Store:
    """get() awaits internally, so unlocked read-modify-writes from
    concurrent tasks deterministically lose updates."""

    def __init__(self):
        self._v = 0

    async def get(self):
        v = self._v
        await asyncio.sleep(0)  # yield to other ready tasks: the race window
        return v

    async def set(self, v):
        self._v = v

    @property
    def raw(self):
        return self._v


def test_safe_add_single_task():
    safe_add = get_attr(load_solution(), "safe_add")

    async def scenario():
        store = Store()
        await safe_add(store, asyncio.Lock(), 7)
        return store.raw

    assert asyncio.run(scenario()) == 7


def test_safe_add_no_lost_updates_under_contention():
    safe_add = get_attr(load_solution(), "safe_add")

    async def scenario():
        store = Store()
        lock = asyncio.Lock()
        await asyncio.gather(*(safe_add(store, lock, 10) for _ in range(5)))
        return store.raw

    assert asyncio.run(scenario()) == 50, (
        "updates were lost — hold the lock around the WHOLE get/add/set"
    )


def test_safe_add_zero_times():
    safe_add = get_attr(load_solution(), "safe_add")

    async def scenario():
        store = Store()
        await safe_add(store, asyncio.Lock(), 0)
        return store.raw

    assert asyncio.run(scenario()) == 0


def test_limiter_bounds_concurrency():
    Limiter = get_attr(load_solution(), "Limiter")
    state = {"active": 0, "peak": 0, "done": 0}

    async def job(limiter):
        async with limiter:
            state["active"] += 1
            state["peak"] = max(state["peak"], state["active"])
            await asyncio.sleep(0.05)
            state["active"] -= 1
        state["done"] += 1

    async def scenario():
        limiter = Limiter(3)
        await asyncio.gather(*(job(limiter) for _ in range(9)))

    asyncio.run(scenario())
    assert state["done"] == 9
    assert state["peak"] <= 3, f"{state['peak']} tasks were inside a Limiter(3)"
    assert state["peak"] == 3, (
        f"peak concurrency was {state['peak']} — a Limiter(3) with 9 eager "
        "tasks should fill all 3 slots, not serialize"
    )


def test_limiter_releases_slot_when_body_raises():
    Limiter = get_attr(load_solution(), "Limiter")

    async def scenario():
        limiter = Limiter(1)
        with pytest.raises(ValueError):
            async with limiter:
                raise ValueError("boom")
        # if the slot leaked, this would deadlock (grader timeout);
        # bound it so failure is a clean assert instead
        async def reenter():
            async with limiter:
                return "ok"

        return await asyncio.wait_for(reenter(), timeout=5)

    assert asyncio.run(scenario()) == "ok"


def test_limiter_limit_one_serializes():
    Limiter = get_attr(load_solution(), "Limiter")
    state = {"active": 0, "peak": 0}

    async def job(limiter):
        async with limiter:
            state["active"] += 1
            state["peak"] = max(state["peak"], state["active"])
            await asyncio.sleep(0.02)
            state["active"] -= 1

    async def scenario():
        limiter = Limiter(1)
        await asyncio.gather(*(job(limiter) for _ in range(4)))

    asyncio.run(scenario())
    assert state["peak"] == 1
