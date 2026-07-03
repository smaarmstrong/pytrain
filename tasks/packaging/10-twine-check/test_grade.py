import subprocess
import sys
import zipfile

import pytest

from pytrain_grader import workspace


@pytest.fixture(scope="session")
def artefacts(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    proc = subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--wheel", "--no-isolation",
         "--outdir", str(out), str(workspace())],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.fail("`python -m build` failed:\n" + (proc.stdout + proc.stderr)[-2000:])
    files = sorted(p for p in out.iterdir() if p.suffix in (".whl", ".gz"))
    if len(files) != 2:
        pytest.fail(f"expected a wheel and an sdist, got: {[f.name for f in out.iterdir()]}")
    return files


def test_twine_check_passes(artefacts):
    proc = subprocess.run(
        [sys.executable, "-m", "twine", "check", *map(str, artefacts)],
        capture_output=True, text=True,
    )
    out = proc.stdout + proc.stderr
    assert "FAILED" not in out, "twine check FAILED:\n" + out
    assert proc.returncode == 0, "twine check exited non-zero:\n" + out
    assert out.count("PASSED") >= 2, \
        "both the wheel and the sdist must PASS twine check:\n" + out


def test_metadata_is_still_sane(artefacts):
    whl = [f for f in artefacts if f.suffix == ".whl"][0]
    with zipfile.ZipFile(whl) as z:
        name = [n for n in z.namelist() if n.endswith(".dist-info/METADATA")][0]
        meta = z.read(name).decode()
    assert "Name: shiny" in meta
    assert "Version: 0.3.0" in meta
    summary = [l for l in meta.splitlines() if l.startswith("Summary:")]
    assert summary and summary[0].split(":", 1)[1].strip(), \
        "keep a non-empty description"


def test_package_still_ships(artefacts):
    whl = [f for f in artefacts if f.suffix == ".whl"][0]
    with zipfile.ZipFile(whl) as z:
        assert "shiny/__init__.py" in z.namelist(), \
            "the shiny package itself must remain in the wheel"
