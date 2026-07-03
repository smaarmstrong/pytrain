# Walking trees with pathlib

Everything here takes `pathlib.Path` objects and must work on any OS — no
string concatenation with `/` or `\\`, no `os.path`. In `solution.py`:

```python
def find_files(root, pattern):
    """All FILES under `root` (recursively, any depth) whose name matches
    the glob `pattern` (e.g. "*.txt", "data_?.csv").

    Return their paths RELATIVE to root, as posix-style strings
    ("sub/dir/a.txt"), sorted alphabetically. Directories whose names
    happen to match must not appear. No matches -> [].
    """

def total_size(root):
    """Total size in bytes of all files under `root`, recursively. 0 for
    an empty tree."""

def backup_path(path):
    """Pure path arithmetic (touch nothing on disk): the Path for a backup
    sibling of `path` — same directory, same name, with ".bak" APPENDED.

    backup_path(Path("a/b/report.txt")) -> Path("a/b/report.txt.bak")
    backup_path(Path("a/b/Makefile"))   -> Path("a/b/Makefile.bak")
    """

def concat_texts(root, out_path):
    """Concatenate every *.txt file under `root` (recursively), in
    sorted-by-relative-posix-path order, and write the result to
    `out_path` (UTF-8). Also RETURN the concatenated string.

    File contents are joined exactly as stored — add nothing between them.
    No .txt files -> write and return "".
    """
```

Example, given `root/notes.txt` = `"alpha\n"` and `root/sub/z.txt` = `"beta\n"`:

```python
>>> find_files(root, "*.txt")
['notes.txt', 'sub/z.txt']
>>> concat_texts(root, out)
'alpha\nbeta\n'
>>> backup_path(Path("a/b/report.txt"))
PosixPath('a/b/report.txt.bak')
```
