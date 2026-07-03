"""Persistence layer: the data file is a JSON array of task dicts."""
import json
from pathlib import Path


def load(path):
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def save(path, tasks):
    Path(path).write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
