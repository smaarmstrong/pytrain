"""access-log analyser CLI."""
import argparse
import sys
from collections import Counter
from pathlib import Path

from parse import parse_line


def build_parser():
    ap = argparse.ArgumentParser(prog="analyse")
    ap.add_argument("logfile")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summary")
    sub.add_parser("status")
    p = sub.add_parser("top")
    p.add_argument("--n", type=int, default=3)
    return ap


def read_log(path):
    entries, skipped = [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = parse_line(line)
        if rec is None:
            skipped += 1
        else:
            entries.append(rec)
    return entries, skipped


def main(argv=None):
    args = build_parser().parse_args(argv)
    path = Path(args.logfile)
    if not path.is_file():
        print(f"error: no such file: {args.logfile}", file=sys.stderr)
        return 1
    entries, skipped = read_log(path)

    if args.cmd == "summary":
        print(f"requests: {len(entries)}")
        print(f"bytes: {sum(e['size'] for e in entries)}")
        print(f"skipped: {skipped}")
    elif args.cmd == "status":
        classes = Counter(e["status"] // 100 for e in entries)
        for c in (2, 3, 4, 5):
            print(f"{c}xx: {classes.get(c, 0)}")
    else:  # top
        paths = Counter(e["path"] for e in entries)
        ranked = sorted(paths.items(), key=lambda kv: (-kv[1], kv[0]))
        for p, count in ranked[: args.n]:
            print(f"{p} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
