"""Local demo — run `python demo.py` to try your crawler on a mock site.

This is how the grader drives your code too: an AsyncClient whose
MockTransport answers everything in-process. No sockets, no network.
"""
import asyncio
import json

import httpx

SITE = {
    "https://site.test/": {"title": "Home", "links": ["https://site.test/a",
                                                      "https://site.test/b"]},
    "https://site.test/a": {"title": "A", "links": ["https://site.test/b"]},
    "https://site.test/b": {"title": "B"},
}


def handler(request):
    page = SITE.get(str(request.url))
    if page is None:
        return httpx.Response(404, json={"error": "not found"})
    return httpx.Response(200, json=page)


async def main():
    from crawler import crawl
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await crawl("https://site.test/", client)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
