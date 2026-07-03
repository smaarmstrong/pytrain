# A [dev] extra for contributors

`mytool` is a small library. End users must get **zero** test tooling when
they `pip install mytool` — but contributors need pytest. The standard
pattern is an *optional dependency group* (an "extra") combined with an
*editable install*:

```bash
# what a contributor runs after cloning:
pip install -e '.[dev]'
```

- `-e` (editable) installs the project as a link to the source tree, so code
  edits take effect without reinstalling;
- `[dev]` pulls in the extra's dependencies on top of the runtime ones.

Your job, in `pyproject.toml` (keep the setuptools backend — the grader
builds with `--no-isolation`):

1. Add a `dev` extra containing `pytest` (version 8 or newer is a sensible
   spec, but any specifier — or none — passes):

   ```toml
   [project.optional-dependencies]
   dev = ["pytest>=8"]
   ```

2. Make sure `pytest` is **not** in the runtime `dependencies` list.

Try the editable install yourself in a scratch venv and check that
`pip show mytool` reports the location inside your workspace.

The grader checks your TOML, then builds a wheel and verifies the *built*
metadata: `Provides-Extra: dev` is present, and every `Requires-Dist` entry
for pytest carries a marker that activates **only** when the `dev` extra is
requested.
