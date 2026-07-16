import importlib.metadata

from pytrain_grader import load_solution, get_attr


def test_reports_an_installed_package():
    f = get_attr(load_solution(), "installed_version")
    # pytest is always present in the grading venv.
    assert f("pytest") == importlib.metadata.version("pytest")


def test_returns_none_when_absent():
    f = get_attr(load_solution(), "installed_version")
    assert f("pytrain-no-such-package-xyz") is None
