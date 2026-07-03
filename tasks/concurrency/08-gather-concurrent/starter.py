import asyncio  # noqa: F401
import time     # noqa: F401


async def fan_out(worker, args_list):
    """gather worker(*args) for every args tuple; ordered results."""
    raise NotImplementedError


async def timed_fan_out(worker, args_list):
    """-> (results, elapsed_seconds)."""
    raise NotImplementedError
