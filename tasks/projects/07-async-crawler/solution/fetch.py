"""Reference: one GET with 503 retry."""


async def fetch_with_retry(client, url, attempts=3):
    resp = None
    for _ in range(attempts):
        resp = await client.get(url)
        if resp.status_code != 503:
            return resp
    return resp
