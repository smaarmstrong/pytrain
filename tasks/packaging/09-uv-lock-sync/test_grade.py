import os
import shutil
import subprocess
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # Rocky/RHEL 9 (3.9) and 3.10 fall back to tomli
    import tomli as tomllib

import pytest

from pytrain_grader import workspace

UV = shutil.which("uv")

pytestmark = pytest.mark.skipif(UV is None, reason="uv is not installed on this machine")


def uv_env(**extra):
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env["UV_PYTHON_DOWNLOADS"] = "never"
    env.update(extra)
    return env


def copy_project(dst):
    dst.mkdir(parents=True, exist_ok=True)
    for name in ("pyproject.toml", "uv.lock", "main.py"):
        src = workspace() / name
        if src.exists():
            shutil.copy(src, dst / name)
    return dst


def test_pyproject_completed():
    path = workspace() / "pyproject.toml"
    if not path.exists():
        pytest.fail("pyproject.toml not found in your workspace")
    proj = tomllib.loads(path.read_text(encoding="utf-8")).get("project", {})
    assert proj.get("name") == "tinyproj"
    assert proj.get("requires-python"), "add requires-python — uv needs it to lock"


def test_lockfile_present_and_plausible():
    lock = workspace() / "uv.lock"
    assert lock.exists(), "no uv.lock in your workspace — run `uv lock`"
    data = tomllib.loads(lock.read_text(encoding="utf-8"))
    assert "version" in data, "uv.lock does not look like a uv lockfile"


def test_lockfile_is_up_to_date(tmp_path):
    proj = copy_project(tmp_path / "proj")
    proc = subprocess.run(
        [UV, "lock", "--check", "--offline", "--no-config"],
        capture_output=True, text=True, cwd=str(proj), env=uv_env(),
    )
    assert proc.returncode == 0, (
        "`uv lock --check` reports the lockfile as missing or stale — "
        "re-run `uv lock` after editing pyproject.toml:\n" + proc.stderr
    )


def test_sync_from_the_lockfile(tmp_path):
    proj = copy_project(tmp_path / "proj")
    venv = tmp_path / "env"
    proc = subprocess.run(
        [UV, "sync", "--locked", "--offline", "--no-config"],
        capture_output=True, text=True, cwd=str(proj),
        env=uv_env(UV_PROJECT_ENVIRONMENT=str(venv)),
    )
    assert proc.returncode == 0, "`uv sync --locked` failed:\n" + proc.stderr
    py = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    assert py.exists(), "uv sync did not create the project environment"
