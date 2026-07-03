"""Slug and whitespace helpers."""
import re


def slugify(text):
    """Lowercase, replace runs of non-alphanumerics with '-', trim dashes."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def squeeze(text):
    """Collapse all internal whitespace runs to single spaces and strip."""
    return re.sub(r"\s+", " ", text).strip()
