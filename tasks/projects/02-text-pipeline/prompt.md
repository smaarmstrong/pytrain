# Project: hashtag report pipeline

A team keeps meeting notes as plain-text files and tags topics inline with
hashtags (`#python`, `#infra-costs`, ...). Build a small pipeline that scans a
directory of notes, regex-extracts the tags, aggregates them with
`collections`, and prints a frequency report.

The entry point is **`report.py`** — the grader runs it as a subprocess
(`python report.py ...`) and inspects stdout, stderr and exit codes.
`extract.py` is scaffolded as a suggested home for the regex layer; only
`report.py`'s behaviour is graded.

## Command-line surface

```
python report.py NOTES_DIR [--top N]
```

## What counts as a tag

A `#` followed by a **letter**, then any run of letters, digits, hyphens or
underscores — i.e. the regex `#([A-Za-z][A-Za-z0-9_-]*)`. Matching is
case-insensitive: normalise every tag to **lowercase** (`#Python` and
`#python` are the same tag). `#42` is *not* a tag (must start with a letter).
Punctuation ends a tag: the line `ship it #python.` contains the tag `python`.

## Behaviour

1. Read every file matching `*.txt` **directly inside** `NOTES_DIR`
   (non-recursive; ignore other extensions and subdirectories). Files are
   UTF-8 text.
2. For each distinct tag aggregate two numbers:
   - **count** — total number of occurrences across all files, and
   - **files** — the number of distinct files the tag appears in
     (a tag used 3 times in one file has count 3, files 1).
3. Print one line per tag to stdout, exactly:

   ```
   #<tag> <count> <files>
   ```

   sorted by **count descending**, ties broken by **tag ascending**
   (alphabetical). With `--top N`, print only the first N lines.
4. A directory with no `.txt` files, or whose files contain no tags: print
   nothing, exit 0.
5. `NOTES_DIR` missing or not a directory: print exactly
   `error: not a directory: <NOTES_DIR>` to **stderr** and exit with code
   **1**.

Use `pathlib` for the filesystem work, `re` for extraction and
`collections.Counter` for the aggregation.

## Acceptance example

With `notes/mon.txt` containing `#Python #infra` on one line and `#python`
on another, and `notes/tue.txt` containing `retro #infra done`:

```
$ python report.py notes
#infra 2 2
#python 2 1
$ python report.py notes --top 1
#infra 2 2
$ python report.py no-such-dir ; echo "exit=$?"
error: not a directory: no-such-dir
exit=1
```

(`infra` and `python` both have count 2; the tie is broken alphabetically.)
