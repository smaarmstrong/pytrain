"""Grades the hashtag pipeline end-to-end: `python report.py DIR` as a real
subprocess against grader-built notes directories."""
from pytrain_grader import run_solution


def report(*args):
    return run_solution(*args, filename="report.py")


def notes(tmp_path, **files):
    d = tmp_path / "notes"
    d.mkdir()
    for name, text in files.items():
        (d / name).write_text(text, encoding="utf-8")
    return d


def test_basic_counts_and_format(tmp_path):
    d = notes(tmp_path, **{
        "mon.txt": "Sprint planning #Python #infra\nDeferred the upgrade again #python\n",
        "tue.txt": "retro #infra done\nbudget review moved to Friday\n",
    })
    r = report(str(d))
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == ["#infra 2 2", "#python 2 1"]


def test_case_insensitive_and_lowercased_output(tmp_path):
    d = notes(tmp_path, **{"a.txt": "#Django #DJANGO #django\n"})
    r = report(str(d))
    assert r.stdout.splitlines() == ["#django 3 1"]


def test_files_column_counts_distinct_files(tmp_path):
    d = notes(tmp_path, **{
        "a.txt": "#x #x #x\n",
        "b.txt": "#x once\n",
        "c.txt": "no tags here\n",
    })
    r = report(str(d))
    assert r.stdout.splitlines() == ["#x 4 2"]


def test_sort_count_desc_then_tag_asc(tmp_path):
    d = notes(tmp_path, **{
        "a.txt": "#zebra #zebra #apple #mango #mango\n",
    })
    r = report(str(d))
    assert r.stdout.splitlines() == [
        "#mango 2 1",
        "#zebra 2 1",
        "#apple 1 1",
    ]


def test_top_limits_output(tmp_path):
    d = notes(tmp_path, **{"a.txt": "#a #a #a #b #b #c\n"})
    r = report(str(d), "--top", "2")
    assert r.returncode == 0
    assert r.stdout.splitlines() == ["#a 3 1", "#b 2 1"]


def test_tag_regex_boundaries(tmp_path):
    d = notes(tmp_path, **{
        "a.txt": "ship it #python. then #infra-costs and #42 nope #py_3\n",
    })
    r = report(str(d))
    assert r.stdout.splitlines() == [
        "#infra-costs 1 1",
        "#py_3 1 1",
        "#python 1 1",
    ]


def test_non_txt_files_and_subdirs_ignored(tmp_path):
    d = notes(tmp_path, **{"a.txt": "#real\n", "b.md": "#markdown\n"})
    sub = d / "sub"
    sub.mkdir()
    (sub / "deep.txt").write_text("#nested\n", encoding="utf-8")
    r = report(str(d))
    assert r.stdout.splitlines() == ["#real 1 1"]


def test_empty_dir_prints_nothing(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    r = report(str(d))
    assert r.returncode == 0
    assert r.stdout == ""


def test_missing_dir_errors(tmp_path):
    missing = tmp_path / "no-such-dir"
    r = report(str(missing))
    assert r.returncode == 1
    assert r.stdout == ""
    assert r.stderr.rstrip("\n") == f"error: not a directory: {missing}"
