import asyncio  # noqa: F401


async def fetch_one(blocking_fn, arg):
    """Run blocking_fn(arg) off the event loop; return its result."""
    raise NotImplementedError


async def fetch_many(blocking_fn, args):
    """Concurrent blocking_fn(arg) for each arg, results in input order."""
    raise NotImplementedError
