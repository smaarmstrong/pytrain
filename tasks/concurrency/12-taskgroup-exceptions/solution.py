import asyncio


async def run_all(coros):
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(c) for c in coros]
    return [t.result() for t in tasks]


async def run_and_summarise(coros):
    try:
        results = await run_all(coros)
    except ExceptionGroup as eg:
        return ("error", sorted(type(e).__name__ for e in eg.exceptions))
    return ("ok", results)
