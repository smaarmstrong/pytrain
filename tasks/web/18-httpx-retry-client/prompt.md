# httpx: a retrying API client

This time you are writing the **client** side. In `solution.py`, write a class
`APIClient` that wraps `httpx.Client` and adds retry behaviour. No server is
involved anywhere — the grader wires in an `httpx.MockTransport`.

```python
class APIClient:
    def __init__(self, base_url, *, transport=None, max_retries=3,
                 timeout=1.0, backoff=0.0):
        ...
    def get_json(self, path):
        ...
    def close(self):
        ...
```

`__init__` builds an internal `httpx.Client` with the given `base_url`,
`timeout`, and — when provided — `transport` (pass it straight through as the
client's `transport=`; that is how the grader intercepts requests).

`get_json(path)` issues `GET` requests for `path` (relative to `base_url`)
until one succeeds, making **at most `max_retries + 1` attempts** in total:

- **2xx** → return the parsed JSON body. Done.
- **5xx** → transient: retry. If the last allowed attempt is still a 5xx,
  raise `httpx.HTTPStatusError` (e.g. via `response.raise_for_status()`).
- **4xx** → the request itself is wrong; raise `httpx.HTTPStatusError`
  **immediately, without retrying**.
- **`httpx.TransportError`** (timeouts, connection failures…) → transient:
  retry. If attempts run out, re-raise the last such exception.

Before each *retry* (not before the first attempt), sleep
`backoff * 2 ** (retry_number - 1)` seconds (retry_number = 1, 2, …). The
default `backoff=0.0` means no sleeping — the grader uses that, so tests are
instant; the parameter just has to be wired correctly.

`close()` closes the underlying `httpx.Client`.

Example (this is roughly what the grader does):

```python
calls = 0
def handler(request):
    global calls
    calls += 1
    if calls < 3:
        return httpx.Response(500)
    return httpx.Response(200, json={"ok": True})

api = APIClient("https://api.test", transport=httpx.MockTransport(handler))
api.get_json("/things")   # -> {"ok": True}, after 3 attempts
```
