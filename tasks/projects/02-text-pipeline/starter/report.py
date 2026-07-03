"""Entry point — the grader runs `python report.py NOTES_DIR [--top N]`.

See prompt.md for the exact output format, sorting and exit codes.
"""
import sys


def main(argv=None):
    # Parse args (NOTES_DIR positional, optional --top N), read the *.txt
    # files, extract tags, aggregate with collections.Counter, print report.
    raise NotImplementedError("see prompt.md")


if __name__ == "__main__":
    sys.exit(main())
