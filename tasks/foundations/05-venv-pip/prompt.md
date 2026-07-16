# Virtual environments and pip

One function in `solution.py` that asks the running Python which packages
it can see — the programmatic version of `pip list`:

```python
def installed_version(package: str) -> str | None:
    """The installed version of `package` (e.g. "8.2.1"), or None if it
    isn't installed in this environment."""
```

Behaviour details:

- Use `importlib.metadata.version(...)` from the standard library — it
  reads the same installation records pip writes. When the package isn't
  installed it raises `importlib.metadata.PackageNotFoundError`; catch
  exactly that and return `None`.
- Return the version **string** exactly as reported; don't parse or
  reformat it.
- The grader runs in a venv that has `pytest` installed, so
  `installed_version("pytest")` returns a version string there, and a
  made-up name returns `None`.

Examples:

```python
>>> installed_version("pytest")     # in an env where pytest is installed
'8.2.1'
>>> installed_version("no-such-package-xyz") is None
True
```
