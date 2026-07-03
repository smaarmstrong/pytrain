"""Text statistics. A word = a run of [a-z0-9']+ after lowercasing."""
import re
from collections import Counter

_WORD = re.compile(r"[a-z0-9']+")


def _words(text):
    return _WORD.findall(text.lower())


def count_words(text):
    return dict(Counter(_words(text)))


def top_words(text, n=5):
    counts = Counter(_words(text))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def summarise(text):
    words = _words(text)
    return {"lines": len(text.splitlines()),
            "words": len(words),
            "unique": len(set(words))}
