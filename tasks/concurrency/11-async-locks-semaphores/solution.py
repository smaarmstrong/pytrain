import asyncio


async def safe_add(store, lock, times):
    for _ in range(times):
        async with lock:
            value = await store.get()
            await store.set(value + 1)


class Limiter:
    def __init__(self, limit):
        self._sem = asyncio.Semaphore(limit)

    async def __aenter__(self):
        await self._sem.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._sem.release()
        return False
