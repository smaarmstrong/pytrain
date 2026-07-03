"""crawl(start_url, client, max_pages=10, concurrency=3) -> {url: title}.

Breadth-first over each page's JSON "links", each distinct URL fetched at
most once via fetch.fetch_with_retry, never more than `concurrency`
requests in flight — but independent pages MUST be fetched concurrently.
Stop after `max_pages` distinct URLs have been fetched. See prompt.md.
"""

from fetch import fetch_with_retry  # noqa: F401  (use this for every page)


async def crawl(start_url, client, max_pages=10, concurrency=3):
    raise NotImplementedError("see prompt.md")
