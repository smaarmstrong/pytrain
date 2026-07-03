# Don't block the loop

Sooner or later async code must call something that *blocks* — a legacy
client, `time.sleep`, file IO. Call it directly inside a coroutine and the
whole event loop freezes: no other task runs until it returns. The bridge
is `asyncio.to_thread(fn, *args)` (or the lower-level
`loop.run_in_executor`), which ships the blocking call to a worker thread
and gives you an awaitable.

In `solution.py`, implement:

```python
async def fetch_one(blocking_fn, arg):
    """Await the BLOCKING function blocking_fn(arg) without blocking the
    event loop; return its result."""

async def fetch_many(blocking_fn, args):
    """Run blocking_fn(arg) for every arg in `args` CONCURRENTLY (each
    bridged off the loop as in fetch_one), and return results IN INPUT
    ORDER. Empty args -> []."""
```

How the grader catches loop-blockers: while your `fetch_many` runs four
0.3-second blocking calls, a heartbeat task on the same loop tries to tick
every 0.05s. A correct bridge keeps the heart beating and finishes in
~0.3s; calling `blocking_fn` directly stops the heartbeat dead and takes
1.2s. Both are asserted.

Example:

```python
def legacy_lookup(key):        # blocking!
    time.sleep(0.1)
    return key.upper()

asyncio.run(fetch_many(legacy_lookup, ["a", "b", "c"]))  # ['A', 'B', 'C'] in ~0.1s
```
