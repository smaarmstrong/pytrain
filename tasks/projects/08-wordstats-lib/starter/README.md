# wordstats — packaging scaffold

src-layout package with a console script:

- `pyproject.toml` — you write it (setuptools backend, `wordstats` 0.1.0,
  `[project.scripts]` entry point, packages found under `src/`).
- `src/wordstats/` — `core.py` (count_words / top_words / summarise),
  `cli.py` (`main(argv=None)`), `__init__.py` re-exports + `__version__`.
- `tests/` — yours; a starter test is included.
- `sample.txt` — matches the acceptance example in the prompt.

The grader builds a real wheel (`python -m build --no-isolation --wheel`),
pip-installs it into a scratch dir, and grades the *installed* package and
`wordstats` script — check the build works before submitting.
