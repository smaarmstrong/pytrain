# Async work crew

The threaded work crew from earlier, reborn in asyncio: a producer feeds an
`asyncio.Queue`, a pool of consumer *tasks* drains it. Same shape, new
plumbing — `await q.put/get`, `q.task_done()`/`await q.join()` (or
sentinels), and `asyncio.create_task` instead of `threading.Thread`.

In `solution.py`, implement:

```python
async def run_pipeline(items, worker, n_consumers):
    """Process every item with the async function `worker` using
    n_consumers consumer tasks fed from one asyncio.Queue.

    - Producer side: put every item on the queue.
    - Consumer side: n_consumers tasks loop, pulling items and awaiting
      worker(item), collecting results.
    - Return the list of results — ORDER DOES NOT MATTER, every item
      processed exactly once.
    - Shut down cleanly: no consumer task may still be alive when this
      returns (sentinels, or queue.join() then cancel the consumers).
    - Handle: empty items, n_consumers=1, more consumers than items.
    """
```

The grader's worker sleeps, so consumers must genuinely overlap waits:
8 items x 0.2s with 4 consumers should take ~0.4s, nowhere near the 1.6s of
one-at-a-time awaiting.

Example:

```python
async def shout(s):
    await asyncio.sleep(0.01)
    return s.upper()

sorted(asyncio.run(run_pipeline(["a", "b"], shout, 2)))  # ['A', 'B']
```
