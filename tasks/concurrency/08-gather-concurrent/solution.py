import asyncio
import time


async def fan_out(worker, args_list):
    return list(await asyncio.gather(*(worker(*args) for args in args_list)))


async def timed_fan_out(worker, args_list):
    start = time.monotonic()
    results = await fan_out(worker, args_list)
    return results, time.monotonic() - start
