# Work crew on a queue

Build the classic producer/consumer pattern: one producer feeds jobs into a
`queue.Queue`, a crew of consumer threads pulls jobs off and processes them.

In `solution.py`, implement:

```python
def run_pipeline(items, process, n_workers):
    """Process every item with `process` using n_workers consumer threads.

    - Put the items on a queue.Queue; n_workers threads consume from it,
      calling process(item) for each and collecting the results.
    - Return a list of all results. ORDER DOES NOT MATTER, but every item
      must be processed exactly once.
    - Shut down cleanly: by the time this function returns, ALL worker
      threads must have terminated (use sentinel values or
      queue.join() + a stop signal — your choice).
    - Must work for an empty `items` list, for n_workers=1, and when
      there are more workers than items.
    """
```

Notes:

- `process` may be slow (it sleeps); with several workers the pipeline must
  actually overlap the waits — the grader times it.
- Appending to a Python list is thread-safe enough for collecting results,
  or protect it with a lock if you prefer.

Example:

```python
>>> sorted(run_pipeline([1, 2, 3], lambda x: x * 10, n_workers=2))
[10, 20, 30]
>>> run_pipeline([], str, n_workers=4)
[]
```
