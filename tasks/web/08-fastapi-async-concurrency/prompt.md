# FastAPI: async endpoints, concurrent work

In `solution.py`, build a FastAPI app (module-level `app`) whose endpoints
are **`async def`** and genuinely concurrent — the grader measures wall
time, so blocking calls (`time.sleep`) or sequential awaits will fail.

Simulated upstream fetch — define this helper and use it from your
endpoints:

```python
import asyncio

DELAY = 0.2

async def fetch_source(name: str) -> dict:
    await asyncio.sleep(DELAY)          # pretend network I/O
    return {"source": name, "length": len(name)}
```

Endpoints:

1. `GET /slow/{name}` — an `async def` endpoint that awaits
   `fetch_source(name)` and returns its dict:
   `{"source": "<name>", "length": <len>}`. Five of these requests fired
   at the same time must finish together (~0.2s total, not ~1s) — the
   event loop must never be blocked.

2. `GET /aggregate?sources=a&sources=b&...` — takes `sources` as a
   **repeated query param** (`list[str]`, at least one required — return
   422 or 400 if absent, hint: `Query(...)`). Fetches **all sources
   concurrently** (e.g. `asyncio.gather`) and returns:

   ```json
   {"results": [{"source": "a", "length": 1}, ...], "count": 2}
   ```

   `results` preserves the order the sources were given in. With 4
   sources this must take ~one `DELAY`, not 4× — the grader allows
   generous margin but a sequential `for ...: await` loop will fail.

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()`
at import time.
