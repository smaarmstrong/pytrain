# side_effect, call counts, autospec: retry logic

Your workspace contains `sync.py`:

```python
def fetch(url): ...              # ALWAYS raises RuntimeError here
def fetch_with_retry(url, attempts=3): ...
```

- `fetch(url)` stands in for a network call; outside production it always
  raises `RuntimeError` — patch it.
- `fetch_with_retry(url, attempts=3)`:
  - calls `fetch(url)` — with exactly that one argument — up to `attempts`
    times;
  - a raised `ConnectionError` means "try again"; the first success returns
    `fetch`'s result immediately (no further calls);
  - if all `attempts` calls raise `ConnectionError`, the last one is
    re-raised;
  - any **other** exception propagates immediately, with no retry.

## Your job

Write `test_sync.py`. The tools this task is about:

- `side_effect` with a **sequence** — e.g.
  `[ConnectionError("down"), ConnectionError("down"), "payload"]` — to script
  fail-fail-succeed scenarios;
- call assertions: `call_count`, `assert_called_once_with(...)`;
- `unittest.mock.create_autospec(sync.fetch)` (or `patch(...,
  autospec=True)`) so a mock that is called with the wrong signature blows up
  instead of silently accepting it.

Scenarios worth scripting: success on the first try; two failures then
success (exactly 3 calls); all attempts exhausted with `attempts=2` (raises
`ConnectionError`, exactly 2 calls); a `ValueError` that must propagate after
exactly 1 call; and everywhere — `fetch` called with `(url,)` and nothing
else.

## How it is graded

Your `test_sync.py` is copied — alone — next to one correct and several buggy
implementations of `sync.py` (an off-by-one extra attempt, no retry at all,
`None` returned instead of re-raising, retrying on *every* exception type,
and calling `fetch` with an extra argument — that last one only an
autospec'd/args-asserted mock will notice). Your suite must pass the correct
one and fail every buggy one. Develop with `python -m pytest -q`.
