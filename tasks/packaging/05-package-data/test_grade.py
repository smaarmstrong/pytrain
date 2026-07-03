import os
import subprocess
import sys
import zipfile

import pytest

from pytrain_grader import workspace


@pytest.fixture(scope="session")
def wheel(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    proc = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation",
         "--outdir", str(out), str(workspace())],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.fail("`python -m build --wheel` failed:\n" + (proc.stdout + proc.stderr)[-2000:])
    wheels = list(out.glob("*.whl"))
    if not wheels:
        pytest.fail("build produced no wheel")
    return wheels[0]


def test_data_file_inside_wheel(wheel):
    with zipfile.ZipFile(wheel) as z:
        names = z.namelist()
    assert "quotes/quotes.txt" in names, (
        "quotes/quotes.txt is not packaged into the wheel — "
        "configure [tool.setuptools.package-data]"
    )


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


def read_quote(installed, n):
    # cwd is the install target, NOT the workspace: the data file must come
    # from the installed package, not the source tree.
    env = os.environ.copy()
    env["PYTHONPATH"] = str(installed)
    return subprocess.run(
        [sys.executable, "-c", f"from quotes import get_quote; print(get_quote({n}))"],
        capture_output=True, text=True, env=env, cwd=str(installed),
    )


def test_reads_data_from_installed_package(installed):
    proc = read_quote(installed, 0)
    assert proc.returncode == 0, \
        f"get_quote(0) failed on the installed package:\n{proc.stderr}"
    assert proc.stdout.strip() == "Simple is better than complex."


def test_middle_and_last_lines(installed):
    proc = read_quote(installed, 3)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "Now is better than never."
    proc = read_quote(installed, 4)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "Namespaces are one honking great idea."
