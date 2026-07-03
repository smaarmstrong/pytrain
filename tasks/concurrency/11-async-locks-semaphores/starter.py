import asyncio  # noqa: F401


async def safe_add(store, lock, times):
    """`times` increments of store (await get / await set), each fully
    guarded by the asyncio.Lock `lock`."""
    raise NotImplementedError


class Limiter:
    """Async context manager admitting at most `limit` concurrent holders."""

    def __init__(self, limit):
        raise NotImplementedError

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError
