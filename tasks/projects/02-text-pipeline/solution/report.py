"""hashtag report — scan a notes directory and print tag frequencies."""
import argparse
import sys
from collections import Counter
from pathlib import Path

from extract import extract_tags


def main(argv=None):
    ap = argparse.ArgumentParser(prog="report")
    ap.add_argument("notes_dir")
    ap.add_argument("--top", type=int, default=None)
    args = ap.parse_args(argv)

    root = Path(args.notes_dir)
    if not root.is_dir():
        print(f"error: not a directory: {args.notes_dir}", file=sys.stderr)
        return 1

    totals = Counter()
    file_counts = Counter()
    for path in sorted(root.glob("*.txt")):
        if not path.is_file():
            continue
        tags = extract_tags(path.read_text(encoding="utf-8"))
        totals.update(tags)
        file_counts.update(set(tags))

    ordered = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    if args.top is not None:
        ordered = ordered[: args.top]
    for tag, count in ordered:
        print(f"#{tag} {count} {file_counts[tag]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
