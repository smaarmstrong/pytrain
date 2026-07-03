import os
import shutil
import tempfile
from pathlib import Path

TRUTHY = {"1", "true", "yes", "on"}


def env_flag(name):
    return os.environ.get(name, "").strip().lower() in TRUTHY


def copy_tree_filtered(src, dst, suffix):
    src = Path(src)
    copied = 0
    for dirpath, _dirnames, filenames in os.walk(src):
        rel = Path(dirpath).relative_to(src)
        target_dir = Path(dst) / rel
        target_dir.mkdir(parents=True, exist_ok=True)
        for fname in filenames:
            if fname.endswith(suffix):
                shutil.copy2(Path(dirpath) / fname, target_dir / fname)
                copied += 1
    return copied


def with_temp_dir(fn):
    with tempfile.TemporaryDirectory() as tmp:
        return fn(Path(tmp))
