import asyncio  # noqa: F401


async def run_all(coros):
    """TaskGroup-run all coros; ordered results, or let the
    ExceptionGroup fly."""
    raise NotImplementedError


async def run_and_summarise(coros):
    """-> ("ok", results) or ("error", sorted exception type names)."""
    raise NotImplementedError
