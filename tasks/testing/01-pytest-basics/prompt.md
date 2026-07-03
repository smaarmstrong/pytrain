# Test slugify against its spec

This is a *test-writing* task: the code is given, **your deliverable is the
test suite**.

Your workspace contains `slugify.py` with one function:

```python
def slugify(text): ...
```

Its contract:

1. The result is lowercase.
2. Any run of spaces and/or underscores becomes a single hyphen `-`.
3. Every other character that is not `a-z`, `0-9` or `-` is removed.
4. Runs of consecutive hyphens collapse to a single hyphen.
5. Leading and trailing hyphens are stripped.
6. `slugify("") == ""`.

Examples:

```python
>>> slugify("Hello, World!")
'hello-world'
>>> slugify("python_is  great")
'python-is-great'
>>> slugify("rock & roll")
'rock-roll'
>>> slugify("  --Already Sluggy--  ")
'already-sluggy'
```

## Your job

Write `test_slugify.py`: a pytest suite that pins down **every rule above**.
Prefer several small, well-named tests over one mega-test.

## How it is graded

Your `test_slugify.py` is copied — alone — into a fresh directory next to
several implementations of `slugify.py`: one correct, and several buggy
(each buggy one violates exactly one rule of the spec). Your suite must
**pass** against the correct implementation and **fail** against every buggy
one.

- Keep everything in `test_slugify.py`; do not rely on `conftest.py` or other
  helper files (they are not copied).
- The `slugify.py` in your workspace is a correct implementation — develop
  against it with `python -m pytest -q`.
