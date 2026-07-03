# Project: todo CLI

Build a small but complete todo manager as a command-line tool. The entry
point is **`todo.py`** — the grader runs it as a subprocess exactly as a user
would (`python todo.py ...`) and inspects stdout, stderr, exit codes and the
JSON data file. A `storage.py` module is scaffolded for the persistence layer;
how you split the code is up to you, only `todo.py`'s behaviour is graded.

## Command-line surface

```
python todo.py [--data-file PATH] add TEXT
python todo.py [--data-file PATH] list [--pending]
python todo.py [--data-file PATH] done ID
python todo.py [--data-file PATH] delete ID
```

- `--data-file PATH` is a **global option and comes before the subcommand**.
  Its default is the value of the `TODO_DATA_FILE` environment variable if
  set, otherwise `todo.json` in the current directory.
- `ID` is an integer (declare it with `type=int`; argparse then exits with
  code **2** on `done abc`, and likewise when no subcommand is given — make
  the subcommand required).

## Behaviour

**`add TEXT`** — appends a new task. Its id is `max(existing ids) + 1`, or
`1` for an empty/missing file (ids of *deleted* tasks may therefore be
reused; that is the specified behaviour). Prints exactly:

```
Added 3: buy milk
```

**`list`** — prints every task in ascending id order, one per line:

```
[ ] 1 buy milk
[x] 2 pay rent
```

`[x]` for done tasks, `[ ]` (a single space) for pending ones. With
`--pending`, done tasks are omitted. An empty or missing data file prints
nothing. Exit code 0 in all these cases.

**`done ID`** — marks the task done and saves. Prints `Done 2: pay rent`.
Marking an already-done task again is fine (same output).

**`delete ID`** — removes the task and saves. Prints `Deleted 2: pay rent`.

**Unknown id** (for `done`/`delete`) — print `error: no task 42` to
**stderr**, exit with code **1**, and leave the data file unchanged.

## Persistence format

The data file is a JSON array of objects, each with exactly the keys
`id` (int), `text` (str), `done` (bool):

```json
[
  {"id": 1, "text": "buy milk", "done": false},
  {"id": 2, "text": "pay rent", "done": true}
]
```

Every mutating command rewrites the file; every command re-reads it first, so
state survives across separate invocations (the grader runs each command as
its own process). A missing file means "no tasks" — never crash on it. Use
`pathlib` for the file handling and the `json` module for (de)serialising.

## Acceptance example

```
$ python todo.py --data-file /tmp/db.json add "buy milk"
Added 1: buy milk
$ python todo.py --data-file /tmp/db.json add "pay rent"
Added 2: pay rent
$ python todo.py --data-file /tmp/db.json done 2
Done 2: pay rent
$ python todo.py --data-file /tmp/db.json list
[ ] 1 buy milk
[x] 2 pay rent
$ python todo.py --data-file /tmp/db.json list --pending
[ ] 1 buy milk
$ python todo.py --data-file /tmp/db.json delete 99 ; echo "exit=$?"
error: no task 99
exit=1
```
