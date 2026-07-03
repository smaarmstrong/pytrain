import asyncio  # noqa: F401


async def run_pipeline(items, worker, n_consumers):
    """Fan items through an asyncio.Queue to n_consumers consumer tasks.
    Return all worker(item) results (any order)."""
    raise NotImplementedError
