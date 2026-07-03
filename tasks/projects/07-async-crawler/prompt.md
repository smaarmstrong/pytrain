# Project: async site crawler

Build a small asynchronous crawler for a JSON "site". There is **no real
network anywhere**: the grader (and your local demo) hand you an
`httpx.AsyncClient` whose transport is an `httpx.MockTransport`, so every
request is answered in-process. Your code must simply use the client it is
given — never create its own connections.

Two modules:

## `fetch.py` — one page, with retry

```python
async def fetch_with_retry(client, url, attempts=3):
    ...
```

- `await client.get(url)` and return the `httpx.Response`.
- If the response status is **503**, try again, up to `attempts` total
  attempts; return the last response if every attempt was 503.
- Any other status (200, 404, 500, ...) is returned **immediately** — no
  retry, no exception.

## `crawler.py` — the crawl

```python
async def crawl(start_url, client, max_pages=10, concurrency=3):
    ...
```

Every page of the site is a JSON document:

```json
{"title": "Home", "links": ["https://site.test/a", "https://site.test/b"]}
```

`links` are absolute URLs and may be absent (treat as `[]`).

Behaviour:

- Start from `start_url` and follow `links` breadth-first, **fetching every
  distinct URL at most once** (dedupe before fetching, including URLs that
  appear in several pages' links).
- Fetch each page via your `fetch_with_retry` (default attempts).
- A page that ends up non-200 contributes nothing: it is **not** in the
  result and its links (if any) are **not** followed.
- Stop once **`max_pages` distinct URLs have been fetched** (successful or
  not) — never fetch URL number `max_pages + 1`.
- **At most `concurrency` requests in flight at any moment** (use e.g.
  `asyncio.Semaphore`), but pages that *can* be fetched in parallel *must*
  be: sibling links waiting on each other one-by-one fails the grader.
- Return a `dict` mapping each successfully fetched URL to its `"title"`.

## Acceptance example

Site: `/` → links `/a`, `/b`; `/a` → links `/b` (already seen); `/b` → no
links; `/missing` referenced nowhere.

```python
result = asyncio.run(crawl("https://site.test/", client))
# {"https://site.test/": "Home",
#  "https://site.test/a": "A",
#  "https://site.test/b": "B"}
# exactly one GET per URL
```

A URL answering 503, 503, 200 (three attempts) ends up in the result; one
answering 503 forever is fetched exactly 3 times and left out.

Try it locally: `python demo.py` runs your crawler against the mock site
defined in `demo.py`.
