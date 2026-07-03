"""Your own tests — extend freely; run with `python -m pytest tests/`.

They need the package importable: either `pip install -e .` in a venv, or
leave the sys.path shim below in place.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from wordstats import count_words  # noqa: E402


def test_counts_case_insensitively():
    assert count_words("The the THE") == {"the": 3}
