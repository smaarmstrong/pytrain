"""quotes — a tiny quote library that ships its data file."""
from importlib import resources


def get_quote(n):
    """Return quote number n (0-based) from the bundled quotes.txt."""
    text = resources.files(__package__).joinpath("quotes.txt").read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[n]
