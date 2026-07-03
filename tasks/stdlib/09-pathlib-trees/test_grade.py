from pathlib import Path

from pytrain_grader import load_solution, get_attr


def make_tree(tmp_path: Path) -> Path:
    root = tmp_path / "root"
    (root / "sub" / "deep").mkdir(parents=True)
    (root / "notes.txt").write_text("alpha\n", encoding="utf-8")
    (root / "data.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (root / "sub" / "z.txt").write_text("beta\n", encoding="utf-8")
    (root / "sub" / "deep" / "a.txt").write_text("gamma", encoding="utf-8")
    # a DIRECTORY whose name matches *.txt — must never be listed as a file
    (root / "sub" / "trap.txt").mkdir()
    return root


def test_find_files_recursive_sorted_relative(tmp_path):
    f = get_attr(load_solution(), "find_files")
    root = make_tree(tmp_path)
    assert f(root, "*.txt") == ["notes.txt", "sub/deep/a.txt", "sub/z.txt"]


def test_find_files_pattern_and_no_match(tmp_path):
    f = get_attr(load_solution(), "find_files")
    root = make_tree(tmp_path)
    assert f(root, "*.csv") == ["data.csv"]
    assert f(root, "*.json") == []


def test_total_size(tmp_path):
    f = get_attr(load_solution(), "total_size")
    root = make_tree(tmp_path)
    # alpha\n (6) + a,b\n1,2\n (8) + beta\n (5) + gamma (5)
    assert f(root) == 24


def test_total_size_empty_tree(tmp_path):
    f = get_attr(load_solution(), "total_size")
    empty = tmp_path / "empty"
    empty.mkdir()
    assert f(empty) == 0


def test_backup_path_arithmetic():
    f = get_attr(load_solution(), "backup_path")
    got = f(Path("a") / "b" / "report.txt")
    assert isinstance(got, Path)
    assert got == Path("a") / "b" / "report.txt.bak"
    assert f(Path("Makefile")) == Path("Makefile.bak")


def test_backup_path_touches_nothing(tmp_path):
    f = get_attr(load_solution(), "backup_path")
    target = tmp_path / "never-created.txt"
    got = f(target)
    assert got.name == "never-created.txt.bak"
    assert list(tmp_path.iterdir()) == []  # nothing was written


def test_concat_texts_order_content_and_file(tmp_path):
    f = get_attr(load_solution(), "concat_texts")
    root = make_tree(tmp_path)
    out = tmp_path / "combined.out"
    got = f(root, out)
    expected = "alpha\n" + "gamma" + "beta\n"  # sorted: notes, sub/deep/a, sub/z
    assert got == expected
    assert out.read_text(encoding="utf-8") == expected


def test_concat_texts_no_txt_files(tmp_path):
    f = get_attr(load_solution(), "concat_texts")
    root = tmp_path / "bare"
    root.mkdir()
    (root / "data.csv").write_text("a,b\n", encoding="utf-8")
    out = tmp_path / "combined.out"
    assert f(root, out) == ""
    assert out.read_text(encoding="utf-8") == ""
