# Author a pyproject.toml

Your workspace contains `greet.py`, a finished single-file module. Your job is
purely packaging: write a `pyproject.toml` next to it so the module builds
into an installable wheel.

Create `pyproject.toml` with:

- A `[build-system]` table using the **setuptools** backend
  (`build-backend = "setuptools.build_meta"`, `requires = ["setuptools>=68"]`).
  The grader builds with `--no-isolation`, so it must be setuptools.
- A `[project]` table declaring:
  - `name = "greet"` and `version = "0.1.0"`
  - a non-empty `description`
  - `requires-python = ">=3.11"`
  - `dependencies` — pretend `greet` needs two runtime packages:
    `colorama` (at least version 0.4) and `packaging` (any version).

Don't rename or edit `greet.py` — setuptools' automatic discovery will pick a
single top-level module up on its own; you don't need any `[tool.setuptools]`
configuration.

Verify locally (optional but recommended):

```bash
pip install build setuptools wheel   # or: uv pip install ...
python -m build --wheel --no-isolation
# dist/greet-0.1.0-py3-none-any.whl should appear, with greet.py inside
```

The grader parses your TOML, checks the metadata and dependency specifiers,
builds a wheel from your workspace, and inspects its contents and METADATA.
