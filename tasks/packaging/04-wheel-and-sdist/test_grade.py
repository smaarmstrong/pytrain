import subprocess
import sys
import tarfile
import zipfile

import pytest

from pytrain_grader import workspace


@pytest.fixture(scope="session")
def dist(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    proc = subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--wheel", "--no-isolation",
         "--outdir", str(out), str(workspace())],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.fail("`python -m build` failed:\n" + (proc.stdout + proc.stderr)[-2000:])
    return out


def wheel_path(dist):
    wheels = list(dist.glob("textkit-1.0.0-*.whl"))
    if not wheels:
        pytest.fail(f"no textkit-1.0.0 wheel was built (got: {[f.name for f in dist.iterdir()]})")
    return wheels[0]


def test_both_artefacts_exist(dist):
    wheel_path(dist)
    assert (dist / "textkit-1.0.0.tar.gz").exists(), \
        f"no textkit-1.0.0.tar.gz sdist was built (got: {[f.name for f in dist.iterdir()]})"


def test_wheel_contents(dist):
    with zipfile.ZipFile(wheel_path(dist)) as z:
        names = z.namelist()
    assert "textkit/__init__.py" in names, "the wheel must contain textkit/__init__.py"
    assert "textkit/slug.py" in names, "the wheel must contain textkit/slug.py"
    assert "textkit-1.0.0.dist-info/METADATA" in names


def test_wheel_metadata(dist):
    with zipfile.ZipFile(wheel_path(dist)) as z:
        meta = z.read("textkit-1.0.0.dist-info/METADATA").decode()
    assert "Name: textkit" in meta
    assert "Version: 1.0.0" in meta
    assert "Description-Content-Type: text/markdown" in meta, \
        'declare readme = "README.md" so the long description is Markdown'
    assert "slugify" in meta, "the README text should be embedded as the long description"


def test_sdist_contents(dist):
    with tarfile.open(dist / "textkit-1.0.0.tar.gz") as tf:
        names = tf.getnames()
    assert "textkit-1.0.0/pyproject.toml" in names, "the sdist must ship pyproject.toml"
    assert "textkit-1.0.0/README.md" in names, "the sdist must ship README.md"
    assert "textkit-1.0.0/textkit/__init__.py" in names, "the sdist must ship the sources"
    assert "textkit-1.0.0/textkit/slug.py" in names, "the sdist must ship the sources"
