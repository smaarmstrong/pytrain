# Streams, asynchronously

`async for` consumes async iterables. You can build them two ways: an
**async generator** (an `async def` containing `yield`) or a class
implementing `__aiter__`/`__anext__` and raising `StopAsyncIteration`.
Build one of each, plus a lazy transformer.

In `solution.py`, implement:

```python
async def ticker(n, interval):
    """Async GENERATOR yielding 0, 1, ..., n-1, awaiting
    asyncio.sleep(interval) before each yield."""

class Countdown:
    """Async ITERATOR (the class itself, via __aiter__/__anext__)
    counting n, n-1, ..., 1, then raising StopAsyncIteration.

    Countdown(3) consumed with `async for` gives 3, 2, 1.
    Each __anext__ awaits asyncio.sleep(0) so it plays nice with the loop.
    """

async def amap(fn, source):
    """Async generator applying the plain function fn to each item of the
    async iterable `source`, LAZILY: pull one item, yield fn(item), pull
    the next only when the consumer asks. Never buffer the whole source.
    """
```

The grader checks laziness for real: it feeds `amap` a source that records
how many items were pulled, takes two results, and expects the source to
have been pulled only a couple of times — materialising it into a list
first fails.

Example:

```python
>>> asyncio.run(_collect(ticker(3, 0.01)))       # [x async for x in ...]
[0, 1, 2]
>>> asyncio.run(_collect(Countdown(3)))
[3, 2, 1]
>>> asyncio.run(_collect(amap(str.upper, ticker_of("ab"))))
['A', 'B']
```
