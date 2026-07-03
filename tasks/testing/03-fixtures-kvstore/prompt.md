# Fixtures with teardown: the key-value store

Your workspace contains `kvstore.py`, a tiny in-process key-value store:

- `kvstore.connect()` returns a `Store`. **At most one store may be open at a
  time** — a second `connect()` while one is open raises `RuntimeError`.
  (Think "single database handle": tests that leak open stores will poison
  every test that runs after them.)
- `store.put(key, value)` — stores the value, **overwriting** any previous
  value for that key.
- `store.get(key)` — returns the value, or raises `KeyError` if absent.
- `store.delete(key)` — returns `True` if the key existed (and removes it),
  `False` if it didn't.
- `store.close()` — releases the connection slot. Calling `close()` again is
  a harmless no-op.
- After `close()`, `put`/`get`/`delete` raise `kvstore.StoreClosed`.

## Your job

Write `test_kvstore.py`, a pytest suite covering the whole contract above:
put/get, overwrite, missing-key behaviour of `get` and `delete`,
delete-existing, behaviour after `close()`, and idempotent close.

Because of the one-open-store rule, **every test must release its store when
it finishes, pass or fail** — that's what fixtures are for:

- write a `store` *yield fixture* that connects, yields, then closes;
- compose fixtures: e.g. a `populated` fixture that takes `store` and
  pre-loads a couple of keys.

A suite that leaks stores will fail against the *correct* implementation —
the grader treats that as a failing submission.

## How it is graded

Your `test_kvstore.py` is copied — alone — next to one correct and several
buggy implementations of `kvstore.py`; it must pass the correct one and fail
every buggy one. Keep everything in `test_kvstore.py` (no `conftest.py`).
Develop against the correct `kvstore.py` in your workspace:
`python -m pytest -q`.
