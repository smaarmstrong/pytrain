import asyncio  # noqa: F401


async def run_with_timeout(coro, seconds):
    """-> ("done", result) or ("timeout", None); cancel the coro on timeout."""
    raise NotImplementedError


async def cancel_after(async_fn, delay):
    """create_task(async_fn()); after `delay`s cancel it if unfinished.
    -> ("finished", result) or ("cancelled", None)."""
    raise NotImplementedError
