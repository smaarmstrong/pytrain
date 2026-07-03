import re
import shutil
import subprocess
import sys
import tomllib
import zipfile

import pytest

from pytrain_grader import workspace


def build_wheel(srcdir, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation",
         "--outdir", str(outdir), str(srcdir)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.fail("`python -m build --wheel` failed:\n" + (proc.stdout + proc.stderr)[-2000:])
    wheels = list(outdir.glob("*.whl"))
    if not wheels:
        pytest.fail("build produced no wheel")
    return wheels[0]


def wheel_version(whl):
    with zipfile.ZipFile(whl) as z:
        name = [n for n in z.namelist() if n.endswith(".dist-info/METADATA")][0]
        meta = z.read(name).decode()
    m = re.search(r"^Version: (.+)$", meta, re.MULTILINE)
    assert m, "wheel METADATA has no Version line"
    return m.group(1).strip()


def test_pyproject_version_is_dynamic():
    path = workspace() / "pyproject.toml"
    if not path.exists():
        pytest.fail("pyproject.toml not found in your workspace")
    proj = tomllib.loads(path.read_text(encoding="utf-8")).get("project", {})
    assert "version" not in proj, \
        "remove the static version from [project] — that's the duplicated source"
    assert "version" in proj.get("dynamic", []), 'declare dynamic = ["version"]'


def test_runtime_dunder_version():
    proc = subprocess.run(
        [sys.executable, "-c", "import boxy; print(boxy.__version__)"],
        capture_output=True, text=True, cwd=str(workspace()),
    )
    assert proc.returncode == 0, f"importing boxy failed:\n{proc.stderr}"
    assert proc.stdout.strip() == "1.2.3"


def test_built_metadata_matches_runtime(tmp_path):
    whl = build_wheel(workspace(), tmp_path / "dist")
    assert wheel_version(whl) == "1.2.3"


def test_bumping_init_bumps_the_build(tmp_path):
    proj = tmp_path / "proj"
    shutil.copytree(workspace(), proj)
    init = proj / "boxy" / "__init__.py"
    if not init.exists():
        pytest.fail("boxy/__init__.py is missing from your workspace")
    src = init.read_text(encoding="utf-8")
    if '__version__ = "1.2.3"' not in src:
        pytest.fail('keep the exact line __version__ = "1.2.3" in boxy/__init__.py '
                    "— the grader bumps it to prove the version is single-sourced")
    init.write_text(
        src.replace('__version__ = "1.2.3"', '__version__ = "9.9.9"'),
        encoding="utf-8",
    )
    whl = build_wheel(proj, tmp_path / "dist")
    assert wheel_version(whl) == "9.9.9", (
        "bumping __version__ in boxy/__init__.py did not change the built "
        "version — the metadata is not single-sourced from the module"
    )
