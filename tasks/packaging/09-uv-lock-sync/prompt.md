# Lock and sync with uv

This task uses the [`uv`](https://docs.astral.sh/uv/) project manager itself
— you need `uv` on your PATH (the grader skips gracefully on machines
without it, but *you* should install it: `pipx install uv` or the official
installer).

`tinyproj` is a minimal application (`main.py`) managed by uv as a
**virtual project** — uv resolves and locks its environment, but the project
itself is never built into a wheel (so there is no build backend at all).

1. Complete `pyproject.toml`:
   - add `requires-python = ">=3.11"` — uv refuses to lock without it;
   - mark the project virtual:

     ```toml
     [tool.uv]
     package = false
     ```

   - do **not** add a `[build-system]` table, and keep `dependencies = []`
     (the point here is the lock/sync workflow, not resolution of real
     packages — and it keeps everything offline-friendly).

2. Produce the lockfile and environment:

   ```bash
   uv lock    # writes uv.lock next to pyproject.toml
   uv sync    # creates .venv from the lockfile
   ```

   `uv.lock` must end up in your workspace, next to `pyproject.toml` (that's
   where `uv lock` writes it; commit-style artefact, don't hand-edit it).

The grader copies `pyproject.toml`, `uv.lock` and `main.py` to a temp
directory and runs `uv lock --check` (the lockfile must exist *and* be up to
date with your pyproject) and `uv sync --locked --offline` into a fresh
environment, asserting the environment gets created.
