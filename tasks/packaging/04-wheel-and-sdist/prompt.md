# Build a wheel and an sdist

Your workspace contains a finished two-module package, `textkit/`, and a
`README.md` — but no `pyproject.toml`, so nothing can be built or shipped.

1. Author `pyproject.toml`:
   - `[build-system]` on the **setuptools** backend
     (`requires = ["setuptools>=68"]`,
     `build-backend = "setuptools.build_meta"`) — the grader builds with
     `--no-isolation`, so it must be setuptools.
   - `[project]`: `name = "textkit"`, `version = "1.0.0"`, a non-empty
     `description`, `requires-python = ">=3.11"`, and
     `readme = "README.md"` so the long description ships as Markdown.

2. Build **both** distribution artefacts yourself and look inside them —
   that's the skill being practised:

   ```bash
   pip install build setuptools wheel      # or: uv build (see below)
   python -m build --no-isolation          # builds sdist AND wheel into dist/
   tar -tzf dist/textkit-1.0.0.tar.gz      # sources + pyproject.toml + README
   unzip -l dist/textkit-1.0.0-py3-none-any.whl
   ```

   (`uv build` does the same job if you prefer uv.)

The grader rebuilds from your workspace and asserts:

- both `textkit-1.0.0-*.whl` and `textkit-1.0.0.tar.gz` are produced;
- the wheel contains `textkit/__init__.py`, `textkit/slug.py`, and METADATA
  with the right name/version and
  `Description-Content-Type: text/markdown`;
- the sdist contains `pyproject.toml`, `README.md`, and the package sources.

Don't modify the `textkit/` modules or `README.md` — only add packaging.
