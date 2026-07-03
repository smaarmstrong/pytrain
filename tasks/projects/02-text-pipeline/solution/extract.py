"""Regex extraction layer."""
import re

TAG_RE = re.compile(r"#([A-Za-z][A-Za-z0-9_-]*)")


def extract_tags(text):
    """Every hashtag in `text`, lowercased, in order of appearance."""
    return [tag.lower() for tag in TAG_RE.findall(text)]
