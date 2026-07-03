# Fan out with gather

`asyncio.gather` starts a batch of awaitables together, lets their waits
overlap, and hands you the results in the order you gave it — not the order
they finished. That's the whole point of this task: five 0.3-second jobs
should take about 0.3 seconds, not 1.5.

In `solution.py`, implement:

```python
async def fan_out(worker, args_list):
    """Run worker(*args) for every args tuple in args_list CONCURRENTLY
    (asyncio.gather) and return the list of results IN INPUT ORDER.

    - `worker` is an async function.
    - args_list is a list of tuples, e.g. [(0.1, "a"), (0.2, "b")].
    - An empty args_list returns [].
    """

async def timed_fan_out(worker, args_list):
    """Like fan_out, but also measure it: return a tuple
    (results, elapsed_seconds) using time.monotonic around the gather."""
```

The grader verifies:

- results come back in input order even when later jobs finish first;
- total wall time for five 0.3s workers is far below the 1.5s a
  sequential loop would take;
- `timed_fan_out`'s reported elapsed time agrees with reality.

Example:

```python
async def slow_echo(delay, value):
    await asyncio.sleep(delay)
    return value

asyncio.run(fan_out(slow_echo, [(0.3, "x"), (0.05, "y")]))  # ['x', 'y'] in ~0.3s
```
