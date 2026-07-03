"""Package tests (also runnable pre-install via the sys.path shim)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from wordstats import count_words, summarise, top_words  # noqa: E402


def test_counts_case_insensitively():
    assert count_words("The the THE") == {"the": 3}


def test_apostrophes_kept_punctuation_splits():
    assert count_words("Don't stop, don't!") == {"don't": 2, "stop": 1}


def test_top_words_ties_alphabetical():
    assert top_words("b a b a c", 2) == [("a", 2), ("b", 2)]


def test_summarise_empty():
    assert summarise("") == {"lines": 0, "words": 0, "unique": 0}
