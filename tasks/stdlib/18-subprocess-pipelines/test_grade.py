import subprocess

import pytest

from pytrain_grader import load_solution, get_attr


def test_run_code_captures_stdout():
    f = get_attr(load_solution(), "run_code")
    out, err, rc = f("print(21 * 2)")
    assert out == "42\n"
    assert err == ""
    assert rc == 0


def test_run_code_captures_stderr_and_exit_code():
    f = get_attr(load_solution(), "run_code")
    out, err, rc = f("import sys; sys.stderr.write('oops'); sys.exit(3)")
    assert out == ""
    assert "oops" in err
    assert rc == 3


def test_run_code_does_not_raise_on_failure():
    f = get_attr(load_solution(), "run_code")
    out, err, rc = f("raise ValueError('boom')")
    assert rc == 1
    assert "ValueError" in err


def test_run_code_returns_text_not_bytes():
    f = get_attr(load_solution(), "run_code")
    out, err, rc = f("print('hi')")
    assert isinstance(out, str) and isinstance(err, str)


def test_checked_output_success():
    f = get_attr(load_solution(), "checked_output")
    assert f("print('ok')") == "ok\n"
    assert f("import sys; sys.stdout.write('no newline')") == "no newline"


def test_checked_output_raises_calledprocesserror():
    f = get_attr(load_solution(), "checked_output")
    with pytest.raises(subprocess.CalledProcessError):
        f("raise SystemExit(1)")
    with pytest.raises(subprocess.CalledProcessError):
        f("import sys; sys.exit(7)")


def test_pipeline_feeds_stdout_to_stdin():
    f = get_attr(load_solution(), "pipeline")
    got = f(
        "print('3'); print('1'); print('2')",
        "import sys; print(sum(int(line) for line in sys.stdin))",
    )
    assert got == "6\n"


def test_pipeline_preserves_stream_shape():
    f = get_attr(load_solution(), "pipeline")
    got = f(
        "import sys; sys.stdout.write('a\\nbb\\nccc\\n')",
        "import sys; [print(len(line.rstrip())) for line in sys.stdin]",
    )
    assert got == "1\n2\n3\n"


def test_pipeline_empty_first_stage():
    f = get_attr(load_solution(), "pipeline")
    got = f("pass", "import sys; print(len(sys.stdin.read()))")
    assert got == "0\n"
