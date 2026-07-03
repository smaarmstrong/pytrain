from pathlib import Path


def find_files(root, pattern):
    root = Path(root)
    return sorted(
        p.relative_to(root).as_posix() for p in root.rglob(pattern) if p.is_file()
    )


def total_size(root):
    return sum(p.stat().st_size for p in Path(root).rglob("*") if p.is_file())


def backup_path(path):
    path = Path(path)
    return path.with_name(path.name + ".bak")


def concat_texts(root, out_path):
    root = Path(root)
    parts = [
        Path(root / rel).read_text(encoding="utf-8")
        for rel in find_files(root, "*.txt")
    ]
    text = "".join(parts)
    Path(out_path).write_text(text, encoding="utf-8")
    return text
