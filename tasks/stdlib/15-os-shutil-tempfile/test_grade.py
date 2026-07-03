from pathlib import Path

import pytest

from pytrain_grader import load_solution, get_attr


# ---- env_flag -------------------------------------------------------------

def test_env_flag_truthy_values(monkeypatch):
    f = get_attr(load_solution(), "env_flag")
    for val in ["1", "true", "TRUE", "Yes", " on ", "YES"]:
        monkeypatch.setenv("PYTRAIN_FLAG", val)
        assert f("PYTRAIN_FLAG") is True, f"{val!r} should be truthy"


def test_env_flag_falsy_values(monkeypatch):
    f = get_attr(load_solution(), "env_flag")
    for val in ["0", "false", "no", "off", "", "2", "yep"]:
        monkeypatch.setenv("PYTRAIN_FLAG", val)
        assert f("PYTRAIN_FLAG") is False, f"{val!r} should be falsy"


def test_env_flag_unset(monkeypatch):
    f = get_attr(load_solution(), "env_flag")
    monkeypatch.delenv("PYTRAIN_MISSING", raising=False)
    assert f("PYTRAIN_MISSING") is False


# ---- copy_tree_filtered -----------------------------------------------------

def make_src(tmp_path):
    src = tmp_path / "src"
    (src / "docs").mkdir(parents=True)
    (src / "logs").mkdir()
    (src / "readme.txt").write_text("root", encoding="utf-8")
    (src / "docs" / "guide.txt").write_text("guide", encoding="utf-8")
    (src / "docs" / "image.png").write_text("png", encoding="utf-8")
    (src / "logs" / "app.log").write_text("log", encoding="utf-8")
    return src


def test_copy_tree_filtered_copies_matching_files(tmp_path):
    f = get_attr(load_solution(), "copy_tree_filtered")
    src, dst = make_src(tmp_path), tmp_path / "dst"
    assert f(src, dst, ".txt") == 2
    assert (dst / "readme.txt").read_text(encoding="utf-8") == "root"
    assert (dst / "docs" / "guide.txt").read_text(encoding="utf-8") == "guide"
    assert not (dst / "docs" / "image.png").exists()
    assert not (dst / "logs" / "app.log").exists()


def test_copy_tree_filtered_recreates_empty_dirs(tmp_path):
    f = get_attr(load_solution(), "copy_tree_filtered")
    src, dst = make_src(tmp_path), tmp_path / "dst"
    f(src, dst, ".txt")
    assert (dst / "logs").is_dir()  # no .txt inside, still recreated


def test_copy_tree_filtered_source_untouched(tmp_path):
    f = get_attr(load_solution(), "copy_tree_filtered")
    src, dst = make_src(tmp_path), tmp_path / "dst"
    before = sorted(p.relative_to(src).as_posix() for p in src.rglob("*"))
    f(src, dst, ".log")
    after = sorted(p.relative_to(src).as_posix() for p in src.rglob("*"))
    assert before == after
    assert (dst / "logs" / "app.log").exists()


# ---- with_temp_dir ----------------------------------------------------------

def test_with_temp_dir_gives_fresh_empty_dir_and_returns_result():
    f = get_attr(load_solution(), "with_temp_dir")
    seen = {}

    def probe(p):
        assert isinstance(p, Path)
        assert p.is_dir()
        assert list(p.iterdir()) == []
        (p / "scratch.txt").write_text("hi", encoding="utf-8")
        seen["path"] = p
        return 42

    assert f(probe) == 42
    assert not seen["path"].exists()  # cleaned up afterwards


def test_with_temp_dir_distinct_dirs_per_call():
    f = get_attr(load_solution(), "with_temp_dir")
    p1 = f(lambda p: p)
    p2 = f(lambda p: p)
    assert p1 != p2


def test_with_temp_dir_cleans_up_on_exception():
    f = get_attr(load_solution(), "with_temp_dir")
    seen = {}

    def boom(p):
        (p / "junk").write_text("x", encoding="utf-8")
        seen["path"] = p
        raise RuntimeError("kaboom")

    with pytest.raises(RuntimeError, match="kaboom"):
        f(boom)
    assert not seen["path"].exists()
