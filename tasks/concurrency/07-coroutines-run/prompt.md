# First coroutines

The asyncio trinity: `async def` defines a coroutine function, `await`
suspends inside one, and `asyncio.run()` is the bridge that lets ordinary
synchronous code drive it all.

In `solution.py`, implement:

```python
async def fetch_value(delay, value):
    """Pretend to fetch something: await asyncio.sleep(delay), then
    return value. (Never time.sleep — that would block the event loop.)"""

async def fetch_all(pairs):
    """pairs is a list of (delay, value) tuples. Await fetch_value for
    each pair ONE AT A TIME, in order, and return the list of values
    in the same order."""

def main(pairs):
    """The synchronous entry point: drive fetch_all(pairs) to completion
    with asyncio.run and return its result. Callers have NO event loop
    running."""
```

Key facts the grader checks:

- `fetch_value` and `fetch_all` are coroutine functions — *calling* them
  runs nothing; they only make progress when awaited.
- `fetch_all` awaits sequentially: three fetches of 0.1s take ~0.3s total
  (running them concurrently comes in the next task).
- `main` works when called from plain synchronous code.

Example:

```python
>>> main([(0.01, "a"), (0.02, "b")])
['a', 'b']
>>> asyncio.run(fetch_value(0.01, 42))   # equivalent low-level use
42
```
