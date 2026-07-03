import asyncio


async def run_with_timeout(coro, seconds):
    try:
        result = await asyncio.wait_for(coro, timeout=seconds)
    except TimeoutError:  # asyncio.TimeoutError is an alias since 3.11
        return ("timeout", None)
    return ("done", result)


async def cancel_after(async_fn, delay):
    task = asyncio.create_task(async_fn())
    await asyncio.sleep(delay)
    if task.done():
        return ("finished", task.result())
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    return ("cancelled", None)
