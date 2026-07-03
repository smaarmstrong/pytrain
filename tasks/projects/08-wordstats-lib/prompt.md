# Project: wordstats — a packaged library

Package a small text-statistics library properly: **src layout**,
**pyproject.toml** (setuptools backend), a **console-script entry point**,
and your own tests. The grader is brutally end-to-end: it builds a wheel
from your workspace (`python -m build --no-isolation --wheel`), installs the
wheel into a scratch directory with `pip install --no-index`, imports the
*installed* package and runs the *installed* `wordstats` script. If it
doesn't build, nothing else is graded.

## Layout

```
pyproject.toml
src/wordstats/__init__.py
src/wordstats/core.py
src/wordstats/cli.py
tests/            # yours to write — run them locally with pytest
```

## `pyproject.toml`

- Build backend: setuptools (`[build-system]` with `requires = ["setuptools"]`
  and `build-backend = "setuptools.build_meta"`).
- Project name **`wordstats`**, version **`0.1.0`**.
- Packages found under `src/` (`[tool.setuptools.packages.find]`,
  `where = ["src"]`).
- Console script: the command **`wordstats`** running your CLI `main`
  (`[project.scripts]`).

## The library (`core.py`, re-exported by `__init__.py`)

A *word* is a maximal run matching `[a-z0-9']+` **after lowercasing** the
text — so `Don't` and `don't` are the same word, and punctuation splits.

```python
count_words(text)      # -> dict {word: count}
top_words(text, n=5)   # -> list of (word, count), count desc, then word asc; at most n
summarise(text)        # -> {"lines": <splitlines count>, "words": <total>, "unique": <distinct>}
```

`from wordstats import count_words, top_words, summarise` must work, and the
package must expose `wordstats.__version__ == "0.1.0"`.
Empty text: `count_words("") == {}`, `summarise("")` is all zeros.

## The CLI (`cli.py`)

`main(argv=None)` — argparse, one positional `file`, option `--top N`
(default 3). Behaviour of `wordstats somefile.txt --top 2`:

- Read the file as UTF-8 text, then print the summary line
  `lines=<L> words=<W> unique=<U>` followed by the top-N words, one
  `<word> <count>` per line (same order as `top_words`).
- If the file doesn't exist: print an error mentioning the path to
  **stderr** and exit with status **2** (nothing on stdout).

```
$ wordstats sample.txt --top 2
lines=2 words=11 unique=7
the 4
cat 2
```

## Check yourself before submitting

```
python -m build --no-isolation --wheel   # must produce dist/wordstats-0.1.0-*.whl
python -m pytest tests/                  # your tests
```
