# Project: access-log analyser

Build a CLI that answers questions about a web server access log in the
Common Log Format. The entry point is **`analyse.py`** — the grader runs it
as a subprocess (`python analyse.py LOGFILE COMMAND ...`) and inspects
stdout, stderr and exit codes. `parse.py` is scaffolded for the line-parsing
layer; only `analyse.py`'s behaviour is graded.

## Log format

One request per line:

```
127.0.0.1 - alice [01/Mar/2026:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 5321
```

i.e. `ip ident user [timestamp] "METHOD path PROTOCOL" status size` where

- `ip`, `ident`, `user` — non-space tokens (`-` when absent),
- `status` — exactly three digits,
- `size` — response bytes: digits, **or `-` meaning 0 bytes**.

A **malformed line** is any non-blank line that doesn't match this shape —
real logs contain garbage; count these but otherwise ignore them. Blank
(whitespace-only) lines are ignored entirely: neither parsed nor counted as
malformed. Parse with a compiled `re` pattern; aggregate with
`collections.Counter`.

## Command-line surface

```
python analyse.py LOGFILE summary
python analyse.py LOGFILE status
python analyse.py LOGFILE top [--n N]
```

`LOGFILE` is a global positional argument and comes before the subcommand;
make the subcommand required (argparse then exits with code **2** when it is
missing or unknown).

**`summary`** — exactly three lines:

```
requests: 9
bytes: 12345
skipped: 2
```

(`requests` = well-formed lines, `bytes` = total size with `-` counted as 0,
`skipped` = malformed lines.)

**`status`** — exactly four lines, one per status class, in this order, with
zero counts included:

```
2xx: 5
3xx: 1
4xx: 2
5xx: 1
```

(You may assume all statuses in the log are 2xx–5xx.)

**`top [--n N]`** (N defaults to 3) — the N most-requested paths, one per
line as `<path> <count>`, sorted by count descending then path ascending.
If fewer than N distinct paths exist, print them all.

**Missing log file** — print `error: no such file: <LOGFILE>` to **stderr**
and exit with code **1** (for any command).

Exit code 0 on success, always.

## Acceptance example

```
$ python analyse.py access.log summary
requests: 5
bytes: 10500
skipped: 1
$ python analyse.py access.log top --n 2
/index.html 3
/about 1
$ python analyse.py gone.log status ; echo "exit=$?"
error: no such file: gone.log
exit=1
```
