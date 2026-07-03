import asyncio
import time

from pytrain_grader import load_solution, get_attr


async def _collect(aiterable):
    return [x async for x in aiterable]


def test_ticker_yields_range():
    ticker = get_attr(load_solution(), "ticker")
    assert asyncio.run(_collect(ticker(4, 0.01))) == [0, 1, 2, 3]
    assert asyncio.run(_collect(ticker(0, 0.01))) == []


def test_ticker_actually_sleeps():
    ticker = get_attr(load_solution(), "ticker")
    start = time.monotonic()
    out = asyncio.run(_collect(ticker(3, 0.1)))
    elapsed = time.monotonic() - start
    assert out == [0, 1, 2]
    assert elapsed >= 0.25, "ticker must await asyncio.sleep(interval) per item"


def test_ticker_is_lazy_via_anext():
    ticker = get_attr(load_solution(), "ticker")

    async def scenario():
        agen = ticker(1000, 0.001)
        first = await anext(agen)
        second = await anext(agen)
        await agen.aclose()
        return first, second

    start = time.monotonic()
    assert asyncio.run(scenario()) == (0, 1)
    # pulling 2 of 1000 items must not pay for all 1000 sleeps (~1s)
    assert time.monotonic() - start < 0.5


def test_countdown_counts_down():
    Countdown = get_attr(load_solution(), "Countdown")
    assert asyncio.run(_collect(Countdown(3))) == [3, 2, 1]
    assert asyncio.run(_collect(Countdown(1))) == [1]
    assert asyncio.run(_collect(Countdown(0))) == []


def test_countdown_protocol_raises_stop():
    Countdown = get_attr(load_solution(), "Countdown")

    async def scenario():
        it = Countdown(1).__aiter__()
        first = await it.__anext__()
        try:
            await it.__anext__()
        except StopAsyncIteration:
            return first, "stopped"
        return first, "kept going"

    assert asyncio.run(scenario()) == (1, "stopped")


def test_amap_maps():
    amap = get_attr(load_solution(), "amap")
    ticker = get_attr(load_solution(), "ticker")
    out = asyncio.run(_collect(amap(lambda x: x * x, ticker(4, 0.001))))
    assert out == [0, 1, 4, 9]


def test_amap_is_lazy():
    amap = get_attr(load_solution(), "amap")
    pulled = []

    async def source():
        for i in range(100):
            pulled.append(i)
            yield i

    async def scenario():
        agen = amap(str, source())
        a = await anext(agen)
        b = await anext(agen)
        await agen.aclose()
        return a, b

    assert asyncio.run(scenario()) == ("0", "1")
    assert len(pulled) <= 3, (
        f"amap pulled {len(pulled)} items to serve 2 — it must not "
        "materialise the source"
    )
