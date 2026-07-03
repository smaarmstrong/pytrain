import asyncio


async def run_pipeline(items, worker, n_consumers):
    q = asyncio.Queue()
    results = []

    async def consumer():
        while True:
            item = await q.get()
            try:
                results.append(await worker(item))
            finally:
                q.task_done()

    consumers = [asyncio.create_task(consumer()) for _ in range(n_consumers)]
    for item in items:
        await q.put(item)
    await q.join()
    for task in consumers:
        task.cancel()
    await asyncio.gather(*consumers, return_exceptions=True)
    return results
