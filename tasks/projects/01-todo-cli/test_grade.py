"""Grades the todo CLI end-to-end: every command is a real subprocess run of
todo.py, state must round-trip through the JSON data file between processes."""
import json

from pytrain_grader import run_solution


def todo(*args, db):
    return run_solution("--data-file", str(db), *args, filename="todo.py")


def test_add_prints_and_creates_json_file(tmp_path):
    db = tmp_path / "db.json"
    r = todo("add", "buy milk", db=db)
    assert r.returncode == 0, r.stderr
    assert r.stdout.rstrip("\n") == "Added 1: buy milk"
    data = json.loads(db.read_text())
    assert data == [{"id": 1, "text": "buy milk", "done": False}]


def test_ids_increment_across_processes(tmp_path):
    db = tmp_path / "db.json"
    todo("add", "a", db=db)
    todo("add", "b", db=db)
    r = todo("add", "c", db=db)
    assert r.stdout.rstrip("\n") == "Added 3: c"


def test_id_is_max_plus_one_after_delete(tmp_path):
    db = tmp_path / "db.json"
    todo("add", "a", db=db)
    todo("add", "b", db=db)
    todo("add", "c", db=db)
    todo("delete", "3", db=db)
    r = todo("add", "d", db=db)
    assert r.stdout.rstrip("\n") == "Added 3: d"  # max(existing)+1 == 3 again


def test_list_output_exact(tmp_path):
    db = tmp_path / "db.json"
    todo("add", "buy milk", db=db)
    todo("add", "pay rent", db=db)
    todo("done", "2", db=db)
    r = todo("list", db=db)
    assert r.returncode == 0
    assert r.stdout.splitlines() == ["[ ] 1 buy milk", "[x] 2 pay rent"]


def test_list_pending_omits_done(tmp_path):
    db = tmp_path / "db.json"
    todo("add", "keep", db=db)
    todo("add", "drop", db=db)
    todo("done", "2", db=db)
    r = todo("list", "--pending", db=db)
    assert r.stdout.splitlines() == ["[ ] 1 keep"]


def test_list_missing_file_prints_nothing(tmp_path):
    r = todo("list", db=tmp_path / "never-created.json")
    assert r.returncode == 0
    assert r.stdout == ""


def test_list_reads_grader_written_file_in_id_order(tmp_path):
    db = tmp_path / "db.json"
    db.write_text(json.dumps([
        {"id": 3, "text": "c", "done": False},
        {"id": 1, "text": "a", "done": True},
    ]))
    r = todo("list", db=db)
    assert r.stdout.splitlines() == ["[x] 1 a", "[ ] 3 c"]


def test_done_marks_and_persists(tmp_path):
    db = tmp_path / "db.json"
    todo("add", "pay rent", db=db)
    r = todo("done", "1", db=db)
    assert r.returncode == 0
    assert r.stdout.rstrip("\n") == "Done 1: pay rent"
    data = json.loads(db.read_text())
    assert data == [{"id": 1, "text": "pay rent", "done": True}]
    # marking an already-done task again is fine, same output
    r = todo("done", "1", db=db)
    assert r.returncode == 0
    assert r.stdout.rstrip("\n") == "Done 1: pay rent"


def test_delete_removes_and_persists(tmp_path):
    db = tmp_path / "db.json"
    todo("add", "a", db=db)
    todo("add", "b", db=db)
    r = todo("delete", "1", db=db)
    assert r.returncode == 0
    assert r.stdout.rstrip("\n") == "Deleted 1: a"
    data = json.loads(db.read_text())
    assert data == [{"id": 2, "text": "b", "done": False}]


def test_unknown_id_errors_leave_file_unchanged(tmp_path):
    db = tmp_path / "db.json"
    todo("add", "only", db=db)
    before = db.read_text()
    for cmd in ("done", "delete"):
        r = todo(cmd, "42", db=db)
        assert r.returncode == 1
        assert r.stdout == ""
        assert r.stderr.rstrip("\n") == "error: no task 42"
        assert db.read_text() == before


def test_argparse_exit_code_2(tmp_path):
    db = tmp_path / "db.json"
    r = todo("done", "abc", db=db)          # non-integer ID
    assert r.returncode == 2
    r = run_solution("--data-file", str(db), filename="todo.py")  # no subcommand
    assert r.returncode == 2
