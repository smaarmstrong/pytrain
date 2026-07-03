# Async site crawler — scaffold

- `fetch.py` — `fetch_with_retry(client, url, attempts=3)`: one GET, 503
  retried up to `attempts` total tries.
- `crawler.py` — `crawl(start_url, client, max_pages=10, concurrency=3)`:
  breadth-first crawl returning `{url: title}`.
- `demo.py` — `python demo.py` runs your crawler against a local mock site
  (exactly how the grader runs it — via `httpx.MockTransport`, no network).

The grader supplies the `httpx.AsyncClient`; your code must use it as-is.
