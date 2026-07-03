# Pull the plug

Real async code has to give up on slow work: bound it with a timeout, or
start it as a task and cancel it yourself. Cancellation is cooperative —
`task.cancel()` throws `asyncio.CancelledError` into the coroutine at its
next `await`, and you must then await the task to let it actually unwind.

In `solution.py`, implement:

```python
async def run_with_timeout(coro, seconds):
    """Await `coro`, but give up after `seconds`.

    Return ("done", result) if it finishes in time.
    On timeout return ("timeout", None) — and make sure the underlying
    coroutine is cancelled, not left running (asyncio.wait_for and the
    asyncio.timeout context manager both do this for you).
    """

async def cancel_after(async_fn, delay):
    """Start async_fn() as a Task with asyncio.create_task, let it run
    for `delay` seconds, then cancel it if it hasn't finished.

    Return ("finished", result) if the task completed before you got to
    cancel it; otherwise cancel, AWAIT the task so it really unwinds
    (swallow only its CancelledError), and return ("cancelled", None).
    """
```

Behaviour the grader checks:

- a fast coroutine under a generous timeout → `("done", result)`;
- a 5-second coroutine under a 0.2s timeout → `("timeout", None)`,
  returning promptly (not after 5s) and the coroutine's
  `except CancelledError` cleanup actually ran;
- `cancel_after` on a long task → `("cancelled", None)`, task cancelled and
  unwound; on a quick task → `("finished", result)`.

Example:

```python
>>> asyncio.run(run_with_timeout(asyncio.sleep(0.01, result="hi"), 1.0))
('done', 'hi')
```
