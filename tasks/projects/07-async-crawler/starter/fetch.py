"""fetch_with_retry(client, url, attempts=3) — one GET with 503 retry.

Return the httpx.Response. Retry only on 503, up to `attempts` total
attempts (return the last 503 response if they all fail). Any other
status returns immediately. See prompt.md.
"""


async def fetch_with_retry(client, url, attempts=3):
    raise NotImplementedError("see prompt.md")
