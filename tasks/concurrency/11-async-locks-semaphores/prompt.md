# Async gatekeepers

Even single-threaded asyncio code has races: every `await` is a door
another task can walk through. You'll fix a read-modify-write race with an
`asyncio.Lock`, and build your own async context manager that bounds
concurrency with an `asyncio.Semaphore`.

In `solution.py`, implement:

```python
async def safe_add(store, lock, times):
    """Increment `store` `times` times, safely.

    `store` has:  `await store.get()` -> int,  `await store.set(v)`.
    One increment = get, add 1, set. Because get() awaits internally,
    unlocked increments from concurrent tasks trample each other — hold
    the asyncio.Lock `lock` (async with) around each COMPLETE
    get-add-set."""

class Limiter:
    """An async context manager admitting at most `limit` concurrent
    holders — a semaphore in a trench coat.

        limiter = Limiter(3)
        async with limiter:
            ...  # at most 3 tasks in here at once

    Implement __init__(self, limit), __aenter__ and __aexit__ (back an
    asyncio.Semaphore, or delegate to one). Must be reusable and shared
    by many tasks; __aexit__ must release even if the body raised."""
```

The grader runs several tasks concurrently through both:

- 5 tasks x 10 `safe_add` increments must land on exactly 50 — the store's
  internal awaits make an unlocked version lose updates *every* time;
- 9 tasks through `Limiter(3)` never see more than 3 inside at once (and
  do reach 3 — a limit-1 serializer fails);
- a task that raises inside `async with limiter` doesn't poison the slot.

Example:

```python
lock = asyncio.Lock()
await asyncio.gather(*(safe_add(store, lock, 10) for _ in range(5)))
await store.get()  # 50
```
