# Pass twine's publish checks

`shiny` is about to be published — but it would land on PyPI with a broken
project page. Before uploading, real projects run:

```bash
pip install build twine setuptools wheel
python -m build --no-isolation
python -m twine check dist/*
```

Do that now: on this project, `twine check` reports **FAILED** — the long
description (the `readme` declared in `pyproject.toml`) is invalid
reStructuredText, so PyPI could not render it.

Fix the project so both built artefacts pass. Either route is acceptable:

- **Recommended**: switch the long description to Markdown — write a small
  `README.md` (a heading and a sentence or two about `shiny.polish()` is
  plenty), and point `readme` at it in `pyproject.toml`. A plain string
  (`readme = "README.md"`) infers the content type from the suffix; delete
  the now-unused `README.rst`.
- Or fix `README.rst` so it renders as valid reStructuredText (the fake
  `.. bogus-directive::` has to go).

Constraints:

- keep `name = "shiny"`, `version = "0.3.0"`, and a non-empty `description`;
- keep the setuptools backend (the grader builds with `--no-isolation`);
- don't change `shiny/__init__.py`.

The grader builds the sdist and wheel from your workspace, runs
`twine check` on both, and requires a clean PASS (plus sane name/version in
the wheel METADATA).
