"""Reference: wave-based BFS crawl with a semaphore concurrency cap."""
import asyncio

from fetch import fetch_with_retry


async def crawl(start_url, client, max_pages=10, concurrency=3):
    sem = asyncio.Semaphore(concurrency)
    results: dict[str, str] = {}
    seen = {start_url}
    frontier = [start_url]
    budget = max_pages

    async def fetch_one(url):
        async with sem:
            resp = await fetch_with_retry(client, url)
        if resp.status_code != 200:
            return url, None, []
        data = resp.json()
        return url, data.get("title"), data.get("links") or []

    while frontier and budget > 0:
        wave = frontier[:budget]
        budget -= len(wave)
        next_frontier = []
        for url, title, links in await asyncio.gather(*(fetch_one(u) for u in wave)):
            if title is not None:
                results[url] = title
            for link in links:
                if link not in seen:
                    seen.add(link)
                    next_frontier.append(link)
        frontier = next_frontier
    return results
