"""Entry point for the todo CLI — the grader runs `python todo.py ...`.

See prompt.md for the full command-line surface, exact output and exit codes.
"""
import sys


def main(argv=None):
    # Build the argparse parser (global --data-file, required subcommand),
    # dispatch to add/list/done/delete, return the exit code.
    raise NotImplementedError("see prompt.md")


if __name__ == "__main__":
    sys.exit(main())
