"""The command-line interface. This file is finished — don't change it."""
import sys


def main(argv=None):
    words = list(sys.argv[1:] if argv is None else argv)
    print(f"{len(words)} words, {len(set(words))} unique")
    return 0
