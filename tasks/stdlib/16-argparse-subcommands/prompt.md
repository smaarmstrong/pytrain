# A tiny calculator CLI

Make `solution.py` a command-line program (the grader runs it as
`python solution.py ...`) built with `argparse` subcommands:

```
python solution.py add A B          # A, B integers -> print A + B
python solution.py div A B          # A, B floats   -> print A / B
python solution.py pow BASE [--exp N]   # ints; N defaults to 2 -> print BASE ** N
```

Behaviour:

- Each command prints exactly one line to **stdout**: the result as
  Python would `print()` it (`add 2 3` -> `5`, `div 7 2` -> `3.5`,
  `pow 2 --exp 10` -> `1024`), and exits with code **0**.
- Let argparse do the input handling — declare `type=int` / `type=float`
  and `default=2`, make the subcommand **required** — and you get the
  error behaviour for free. All of these must exit with code **2** and
  print a message to **stderr** (nothing to stdout):
  - no subcommand at all
  - an unknown subcommand
  - a missing argument (`add 2`)
  - a non-numeric argument (`add two 3`, `pow 2 --exp x`)
- `python solution.py --help` exits 0 and mentions all three
  subcommands on stdout.

Examples:

```console
$ python solution.py add 2 3
5
$ python solution.py pow 3
9
$ python solution.py add two 3; echo "exit=$?"
usage: ...
exit=2
```
