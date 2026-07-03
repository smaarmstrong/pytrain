"""Entry point — the grader runs `python analyse.py LOGFILE COMMAND ...`.

See prompt.md for the exact commands, output format and exit codes.
"""
import sys


def main(argv=None):
    # argparse: LOGFILE positional + required subcommand (summary/status/top),
    # parse the log, aggregate with collections.Counter, print the report.
    raise NotImplementedError("see prompt.md")


if __name__ == "__main__":
    sys.exit(main())
