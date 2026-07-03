# All or nothing with TaskGroup

`asyncio.TaskGroup` (3.11+) is structured concurrency: tasks started in the
group cannot outlive it, the first failure cancels every sibling, and the
failures arrive bundled in an `ExceptionGroup`.

In `solution.py`, implement:

```python
async def run_all(coros):
    """Run every coroutine in `coros` concurrently inside an
    asyncio.TaskGroup.

    If they all succeed, return their results in input order.
    If any fail, DON'T catch anything: let the TaskGroup's
    ExceptionGroup propagate to the caller (siblings get cancelled by
    the group — that's the point)."""

async def run_and_summarise(coros):
    """Like run_all, but absorb failure into a summary value:

    - all succeed  -> ("ok", [results in input order])
    - any fail     -> ("error", sorted list of exception TYPE NAMES from
                       the ExceptionGroup, e.g. ["KeyError", "ValueError"])

    Catch the ExceptionGroup (`except* ...` or a plain except around the
    group) and inspect its .exceptions."""
```

The grader checks:

- success path returns ordered results;
- on failure, `run_all` raises an `ExceptionGroup` containing the original
  error, promptly — and the still-sleeping sibling coroutines observe
  `CancelledError` (i.e. the group really cancelled them);
- `run_and_summarise` turns the same situation into an
  `("error", [...])` summary and never lets the group escape.

Example:

```python
>>> asyncio.run(run_all([sleepy("a"), sleepy("b")]))
['a', 'b']
>>> asyncio.run(run_and_summarise([sleepy("a"), kaboom()]))
('error', ['ValueError'])
```
