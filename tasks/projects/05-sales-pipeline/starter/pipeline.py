"""Entry point — the grader runs `python pipeline.py INPUT_CSV OUTPUT_DB`.

Read the CSV with pandas, clean it (see clean.py), write the `sales` and
`summary` tables into the SQLite db, print the report. See prompt.md for
the exact schemas, output format and exit codes.
"""
import sys


def main(argv=None):
    raise NotImplementedError("see prompt.md")


if __name__ == "__main__":
    sys.exit(main())
