"""A correct implementation of the spec in prompt.md — write tests for it."""
import re


def slugify(text):
    text = text.lower()
    text = re.sub(r"[ _]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")
