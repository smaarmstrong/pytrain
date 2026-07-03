import asyncio


async def fetch_value(delay, value):
    await asyncio.sleep(delay)
    return value


async def fetch_all(pairs):
    results = []
    for delay, value in pairs:
        results.append(await fetch_value(delay, value))
    return results


def main(pairs):
    return asyncio.run(fetch_all(pairs))
