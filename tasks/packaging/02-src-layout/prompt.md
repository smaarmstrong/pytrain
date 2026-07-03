# Restructure into a src/ layout

Your workspace holds `textstats.py`, a flat single-file module, plus a
`pyproject.toml` that is already configured for a **src layout**
(`[tool.setuptools.packages.find] where = ["src"]`). As it stands the project
doesn't even build-and-import correctly — there is no `src/` yet.

Restructure it, without changing any behaviour:

1. Create the package `src/textstats/`.
2. Move the three functions' implementations into `src/textstats/stats.py`
   (the `words()` helper can go wherever you like).
3. Make `src/textstats/__init__.py` re-export the public API so both of these
   work after installation:

   ```python
   from textstats import word_count, unique_words, top_words
   from textstats.stats import top_words
   ```

4. Delete the flat `textstats.py` from the workspace root — that's the point
   of the exercise: the importable code lives only under `src/`.

Leave `pyproject.toml`'s src-layout configuration in place (you may edit other
metadata if you want, but the package must keep installing from `src/`).

Verify locally (optional): `pip install -e .` in a scratch venv, then from any
other directory run
`python -c "from textstats import word_count; print(word_count('a b'))"` → `2`.

The grader pip-installs your workspace into a temporary directory (offline,
no build isolation — setuptools is preinstalled) and imports the installed
package from a subprocess, checking `word_count`, `unique_words`,
`top_words`, and `textstats.stats`.
