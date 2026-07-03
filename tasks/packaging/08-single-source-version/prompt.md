# Single-source the version

The `boxy` project states its version **twice**: once as
`__version__ = "1.2.3"` in `boxy/__init__.py`, and again as
`version = "1.2.3"` in `pyproject.toml`. That's a release-day landmine — bump
one and forget the other, and PyPI metadata disagrees with
`boxy.__version__` at runtime.

Fix it so `boxy/__init__.py` is the **only** place the version is written:

1. Keep the exact line `__version__ = "1.2.3"` in `boxy/__init__.py`
   (the grader edits this line in a copy of your project, so keep its exact
   shape).
2. In `pyproject.toml`, remove the static `version` from `[project]` and
   declare it dynamic, sourced from the package attribute. With the
   setuptools backend (keep it — the grader builds with `--no-isolation`):

   ```toml
   [project]
   dynamic = ["version"]

   [tool.setuptools.dynamic]
   version = {attr = "boxy.__version__"}
   ```

Behaviour that must hold afterwards:

- `python -c "import boxy; print(boxy.__version__)"` → `1.2.3`
- a built wheel's METADATA says `Version: 1.2.3`
- **the real test**: if `__version__` in `boxy/__init__.py` is changed to
  `"9.9.9"` and the project rebuilt, the wheel's METADATA version follows
  automatically. The grader does exactly this in a temporary copy of your
  workspace.

Don't change `boxy.box()` — it's finished.
