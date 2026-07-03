"""A correct implementation of the spec in prompt.md — write tests for it."""
import json
import os


def save_config(path, cfg):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f)


def load_config(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_setting(name, default=None):
    raw = os.environ.get("APP_" + name.upper())
    if raw is None:
        return default
    low = raw.lower()
    if low in ("true", "false"):
        return low == "true"
    if raw.isdigit():
        return int(raw)
    return raw
