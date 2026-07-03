import asyncio


async def fetch_one(blocking_fn, arg):
    return await asyncio.to_thread(blocking_fn, arg)


async def fetch_many(blocking_fn, args):
    return list(await asyncio.gather(*(fetch_one(blocking_fn, a) for a in args)))
