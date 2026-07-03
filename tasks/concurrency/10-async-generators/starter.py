import asyncio  # noqa: F401


async def ticker(n, interval):
    """Async generator: yield 0..n-1, sleeping `interval` before each."""
    raise NotImplementedError
    yield  # noqa — makes this an async generator; remove when implementing


class Countdown:
    """Async iterator: n, n-1, ..., 1 via __aiter__/__anext__."""

    def __init__(self, n):
        raise NotImplementedError


async def amap(fn, source):
    """Lazily yield fn(item) for each item of async iterable `source`."""
    raise NotImplementedError
    yield  # noqa — makes this an async generator; remove when implementing
