# Wire up a console script

Your workspace is a small, finished package:

- `wordcli/cli.py` defines `main(argv=None)` — it prints a summary like
  `3 words, 2 unique` for the words it is given (from `argv`, falling back to
  `sys.argv[1:]`).
- `pyproject.toml` has complete metadata but installs **no command**.

Add a *console script* entry point so that installing the project puts a
`wordcli` command on the user's PATH, implemented by `wordcli.cli:main`.
That's the `[project.scripts]` table in `pyproject.toml`:

```toml
[project.scripts]
<command-name> = "<module.path>:<function>"
```

Don't change `wordcli/cli.py` — the CLI behaviour is already correct.

Verify locally (optional): in a scratch venv, `pip install .` then:

```console
$ wordcli hello world hello
3 words, 2 unique
```

The grader installs your project into a temporary directory (offline) and
checks two things: the installed distribution's metadata declares a
`console_scripts` entry point named `wordcli`, and loading that entry point
via `importlib.metadata` and calling it with `["hello", "world", "hello"]`
prints `3 words, 2 unique`.
