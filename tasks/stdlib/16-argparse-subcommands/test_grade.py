from pytrain_grader import run_solution


def test_add():
    proc = run_solution("add", "2", "3")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "5"


def test_add_negative():
    proc = run_solution("add", "-4", "1")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "-3"


def test_div_float_semantics():
    proc = run_solution("div", "7", "2")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "3.5"
    proc = run_solution("div", "1", "4")
    assert proc.stdout.strip() == "0.25"


def test_pow_default_exponent_is_2():
    proc = run_solution("pow", "3")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "9"


def test_pow_explicit_exponent():
    proc = run_solution("pow", "2", "--exp", "10")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "1024"


def test_no_subcommand_exits_2():
    proc = run_solution()
    assert proc.returncode == 2
    assert proc.stderr.strip() != ""
    assert proc.stdout.strip() == ""


def test_unknown_subcommand_exits_2():
    proc = run_solution("frobnicate", "1")
    assert proc.returncode == 2
    assert proc.stderr.strip() != ""


def test_missing_argument_exits_2():
    proc = run_solution("add", "2")
    assert proc.returncode == 2
    assert proc.stderr.strip() != ""


def test_non_numeric_argument_exits_2():
    proc = run_solution("add", "two", "3")
    assert proc.returncode == 2
    assert proc.stderr.strip() != ""
    proc = run_solution("pow", "2", "--exp", "x")
    assert proc.returncode == 2


def test_help_lists_subcommands():
    proc = run_solution("--help")
    assert proc.returncode == 0
    for name in ("add", "div", "pow"):
        assert name in proc.stdout
