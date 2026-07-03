import importlib.metadata
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace


@pytest.fixture(scope="session")
def installed(tmp_path_factory):
    target = tmp_path_factory.mktemp("site")
    proc = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet",
         "--no-build-isolation", "--no-index",
         "--target", str(target), str(workspace())],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.fail("pip install of your project failed:\n" + (proc.stdout + proc.stderr)[-2000:])
    return target


def find_entry_point(installed):
    for dist in importlib.metadata.distributions(path=[str(installed)]):
        for ep in dist.entry_points:
            if ep.group == "console_scripts" and ep.name == "wordcli":
                return ep
    return None


def test_console_script_declared(installed):
    ep = find_entry_point(installed)
    assert ep is not None, (
        "the installed metadata declares no console script named `wordcli` — "
        "did you add [project.scripts]?"
    )


def test_console_script_runs(installed):
    code = (
        "import contextlib, io, importlib.metadata\n"
        "eps = [e for e in importlib.metadata.entry_points(group='console_scripts')\n"
        "       if e.name == 'wordcli']\n"
        "assert eps, 'wordcli entry point not found on sys.path'\n"
        "fn = eps[0].load()\n"
        "buf = io.StringIO()\n"
        "with contextlib.redirect_stdout(buf):\n"
        "    try:\n"
        "        fn(['hello', 'world', 'hello'])\n"
        "    except SystemExit:\n"
        "        pass\n"
        "print(buf.getvalue().strip())\n"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(installed)
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, env=env, cwd=str(installed),
    )
    assert proc.returncode == 0, f"loading/running the entry point failed:\n{proc.stderr}"
    assert proc.stdout.strip() == "3 words, 2 unique"


def test_console_script_empty_args(installed):
    code = (
        "import contextlib, io, importlib.metadata\n"
        "eps = [e for e in importlib.metadata.entry_points(group='console_scripts')\n"
        "       if e.name == 'wordcli']\n"
        "fn = eps[0].load()\n"
        "buf = io.StringIO()\n"
        "with contextlib.redirect_stdout(buf):\n"
        "    try:\n"
        "        fn([])\n"
        "    except SystemExit:\n"
        "        pass\n"
        "print(buf.getvalue().strip())\n"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(installed)
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, env=env, cwd=str(installed),
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "0 words, 0 unique"
