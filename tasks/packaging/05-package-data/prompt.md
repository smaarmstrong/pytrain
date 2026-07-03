# Ship a data file inside the wheel

The `quotes` package in your workspace bundles a text file,
`quotes/quotes.txt` — but two things are broken:

1. **The wheel doesn't include it.** By default setuptools packages only
   `.py` files. Configure package data in `pyproject.toml` (the backend is
   setuptools — keep it that way, the grader builds with `--no-isolation`):

   ```toml
   [tool.setuptools.package-data]
   quotes = ["*.txt"]
   ```

2. **`get_quote` isn't implemented.** In `quotes/__init__.py` implement:

   ```python
   def get_quote(n):
       """Return quote number n (0-based) from the bundled quotes.txt."""
   ```

   - Read the file through **`importlib.resources`** (`resources.files(...)`),
     *not* by building paths from `__file__` — resource reading must work
     however the package is installed.
   - Quotes are the non-empty lines of `quotes.txt`, in order, with
     surrounding whitespace stripped. `n` indexes that list.

Example (after `pip install .` in a scratch venv, from any directory):

```python
>>> from quotes import get_quote
>>> get_quote(0)
'Simple is better than complex.'
>>> get_quote(3)
'Now is better than never.'
```

Don't edit `quotes/quotes.txt`. The grader builds a wheel from your workspace
and asserts `quotes/quotes.txt` is inside it, then pip-installs the project
into a temp directory and calls `get_quote` from a subprocess running
*outside* your workspace — so it only passes if the data file really ships
and is read via the installed package's resources.
