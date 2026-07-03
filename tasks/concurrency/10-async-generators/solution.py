import asyncio


async def ticker(n, interval):
    for i in range(n):
        await asyncio.sleep(interval)
        yield i


class Countdown:
    def __init__(self, n):
        self._current = n

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._current < 1:
            raise StopAsyncIteration
        await asyncio.sleep(0)
        value = self._current
        self._current -= 1
        return value


async def amap(fn, source):
    async for item in source:
        yield fn(item)
