# Env vars, tree copies, disposable dirs

Three OS chores done properly with `os`, `shutil` and `tempfile`. In
`solution.py`:

```python
def env_flag(name):
    """Read environment variable `name` as a boolean flag.

    "1", "true", "yes", "on" (any case, surrounding whitespace ignored)
    -> True. Anything else — including unset — -> False.
    """

def copy_tree_filtered(src, dst, suffix):
    """Copy the directory tree at `src` to `dst` (which does not exist
    yet), keeping ONLY files whose name ends with `suffix` — but
    recreating EVERY directory of the tree, even ones left empty.

    Relative layout is preserved. Return the number of files copied.
    """

def with_temp_dir(fn):
    """Create a fresh temporary directory (somewhere under the system
    temp location, e.g. via tempfile), call fn(path) with it as a
    pathlib.Path, and return fn's result.

    The directory must exist and be empty when fn sees it, and must be
    GONE afterwards — even when fn raises (let the exception propagate
    after cleanup).
    """
```

Example:

```python
>>> os.environ["DEBUG"] = " YES "
>>> env_flag("DEBUG"), env_flag("NOPE")
(True, False)
>>> copy_tree_filtered(src, dst, ".txt")   # src has 2 .txt, 1 .log
2
>>> with_temp_dir(lambda p: (p / "x").write_text("hi"))
2
```
