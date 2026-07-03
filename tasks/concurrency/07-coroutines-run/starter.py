import asyncio  # noqa: F401


async def fetch_value(delay, value):
    """await asyncio.sleep(delay), return value."""
    raise NotImplementedError


async def fetch_all(pairs):
    """Await fetch_value for each (delay, value) pair sequentially;
    return the values in order."""
    raise NotImplementedError


def main(pairs):
    """Synchronous entry point: asyncio.run the fetch_all coroutine."""
    raise NotImplementedError
