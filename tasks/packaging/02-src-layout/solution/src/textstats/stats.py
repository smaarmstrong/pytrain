"""Implementations for textstats."""
import collections
import re


def words(text):
    """All lowercase words in `text` (letters and apostrophes)."""
    return re.findall(r"[a-z']+", text.lower())


def word_count(text):
    """How many words `text` contains."""
    return len(words(text))


def unique_words(text):
    """Sorted list of the distinct words in `text`."""
    return sorted(set(words(text)))


def top_words(text, n=3):
    """The n most common words as (word, count) pairs, most common first."""
    return collections.Counter(words(text)).most_common(n)
