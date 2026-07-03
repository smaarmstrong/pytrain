"""Console entry point: wordstats FILE [--top N]."""
import argparse
import sys
from pathlib import Path

from .core import summarise, top_words


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordstats")
    parser.add_argument("file")
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.exists():
        print(f"error: {path} not found", file=sys.stderr)
        sys.exit(2)
    text = path.read_text(encoding="utf-8")

    s = summarise(text)
    print(f"lines={s['lines']} words={s['words']} unique={s['unique']}")
    for word, count in top_words(text, args.top):
        print(f"{word} {count}")


if __name__ == "__main__":
    main()
