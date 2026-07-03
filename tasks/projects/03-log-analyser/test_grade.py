"""Grades the log analyser end-to-end: every command is a real subprocess run
of analyse.py against a grader-written fixture log."""
import pytest

from pytrain_grader import run_solution

LOG = """\
1.1.1.1 - - [01/Mar/2026:10:00:00 +0000] "GET / HTTP/1.1" 200 100
1.1.1.1 - alice [01/Mar/2026:10:00:01 +0000] "GET / HTTP/1.1" 200 200
2.2.2.2 - - [01/Mar/2026:10:00:02 +0000] "GET /about HTTP/1.1" 200 300
2.2.2.2 - - [01/Mar/2026:10:00:03 +0000] "GET / HTTP/1.1" 304 -
this is not a log line

3.3.3.3 - bob [01/Mar/2026:10:00:04 +0000] "POST /login HTTP/1.1" 302 50
3.3.3.3 - bob [01/Mar/2026:10:00:05 +0000] "GET /missing HTTP/1.1" 404 25
3.3.3.3 - bob [01/Mar/2026:10:00:06 +0000] "GET /about HTTP/1.1" 404 25
5.5.5.5 - - [01/Mar/2026:10:00:08 +0000] "GET /truncated
4.4.4.4 - - [01/Mar/2026:10:00:07 +0000] "GET /boom HTTP/1.1" 500 999
"""
# well-formed: 8 requests; bytes 100+200+300+0+50+25+25+999 = 1699
# malformed: 2 (garbage line + truncated line); blank line ignored entirely


@pytest.fixture()
def logfile(tmp_path):
    p = tmp_path / "access.log"
    p.write_text(LOG, encoding="utf-8")
    return p


def analyse(*args):
    return run_solution(*args, filename="analyse.py")


def test_summary(logfile):
    r = analyse(str(logfile), "summary")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == [
        "requests: 8",
        "bytes: 1699",
        "skipped: 2",
    ]


def test_summary_empty_file(tmp_path):
    p = tmp_path / "empty.log"
    p.write_text("", encoding="utf-8")
    r = analyse(str(p), "summary")
    assert r.returncode == 0
    assert r.stdout.splitlines() == ["requests: 0", "bytes: 0", "skipped: 0"]


def test_status_classes_with_zero_counts(logfile):
    r = analyse(str(logfile), "status")
    assert r.returncode == 0
    assert r.stdout.splitlines() == ["2xx: 3", "3xx: 2", "4xx: 2", "5xx: 1"]


def test_status_all_zero_but_2xx(tmp_path):
    p = tmp_path / "ok.log"
    p.write_text(
        '9.9.9.9 - - [01/Mar/2026:11:00:00 +0000] "GET /a HTTP/1.1" 200 10\n',
        encoding="utf-8",
    )
    r = analyse(str(p), "status")
    assert r.stdout.splitlines() == ["2xx: 1", "3xx: 0", "4xx: 0", "5xx: 0"]


def test_top_default_three(logfile):
    r = analyse(str(logfile), "top")
    assert r.returncode == 0
    assert r.stdout.splitlines() == ["/ 3", "/about 2", "/boom 1"]


def test_top_n_all_ties_alphabetical(logfile):
    r = analyse(str(logfile), "top", "--n", "10")
    assert r.stdout.splitlines() == [
        "/ 3",
        "/about 2",
        "/boom 1",
        "/login 1",
        "/missing 1",
    ]


def test_top_n_one(logfile):
    r = analyse(str(logfile), "top", "--n", "1")
    assert r.stdout.splitlines() == ["/ 3"]


def test_missing_file_errors(tmp_path):
    missing = tmp_path / "gone.log"
    r = analyse(str(missing), "status")
    assert r.returncode == 1
    assert r.stdout == ""
    assert r.stderr.rstrip("\n") == f"error: no such file: {missing}"


def test_argparse_exit_code_2(logfile):
    r = analyse(str(logfile))  # no subcommand
    assert r.returncode == 2
    r = analyse(str(logfile), "frobnicate")  # unknown subcommand
    assert r.returncode == 2
