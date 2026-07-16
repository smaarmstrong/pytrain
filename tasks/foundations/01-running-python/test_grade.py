from pytrain_grader import run_solution


def test_script_runs_cleanly():
    proc = run_solution()
    assert proc.returncode == 0, f"the script errored:\n{proc.stderr}"


def test_prints_exactly_the_two_lines():
    proc = run_solution()
    assert proc.stdout == "hello from pytrain\nthe answer is 42\n"
