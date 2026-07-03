# tmp_path and monkeypatch: config loader

Your workspace contains `confload.py`:

```python
def save_config(path, cfg): ...   # write cfg (a dict) to path as JSON
def load_config(path): ...        # read it back
def get_setting(name, default=None): ...  # read one setting from the environment
```

Contract:

- `save_config(path, cfg)` writes `cfg` as JSON; `load_config(path)` reads it
  back — a **round-trip preserves values and their types** (`3` stays an
  `int`, `True` stays a `bool`).
- `load_config(path)` returns `{}` when the file does not exist (no error).
- `get_setting(name, default=None)` reads the environment variable
  `APP_<NAME>` — the name is uppercased, e.g. `get_setting("timeout")` reads
  `APP_TIMEOUT`. Then:
  - variable unset → return `default`;
  - value is `"true"`/`"false"` (any case) → return the Python bool;
  - value is all digits → return an `int`;
  - anything else → return the string unchanged.

## Your job

Write `test_confload.py` covering the whole contract, using pytest's built-in
fixtures:

- `tmp_path` for the file round-trip and the missing-file case — never touch
  the current directory;
- `monkeypatch.setenv` / `monkeypatch.delenv(..., raising=False)` for the
  environment cases — never leave env vars behind after a test.

## How it is graded

Your `test_confload.py` is copied — alone — next to one correct and several
buggy implementations of `confload.py` (crashes on a missing file, saves
everything as strings, ignores the environment, forgets to uppercase, skips
the bool/int conversions). It must pass the correct one and fail every buggy
one. Keep everything in `test_confload.py`; develop against the correct
`confload.py` in your workspace with `python -m pytest -q`.
