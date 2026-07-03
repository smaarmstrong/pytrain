import datetime
import json
from pathlib import Path


def _default(o):
    if isinstance(o, set):
        return {"__kind__": "set", "items": sorted(o, key=repr)}
    if isinstance(o, datetime.date):
        return {"__kind__": "date", "iso": o.isoformat()}
    raise TypeError(f"not JSON serialisable: {type(o).__name__}")


def _hook(d):
    kind = d.get("__kind__")
    if kind == "set":
        return set(d["items"])
    if kind == "date":
        return datetime.date.fromisoformat(d["iso"])
    return d


def to_json(obj):
    return json.dumps(obj, default=_default)


def from_json(s):
    return json.loads(s, object_hook=_hook)


def save(obj, path):
    Path(path).write_text(to_json(obj), encoding="utf-8")


def load(path):
    return from_json(Path(path).read_text(encoding="utf-8"))
