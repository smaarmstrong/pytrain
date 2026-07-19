import subprocess
import sys
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # Rocky/RHEL 9 (3.9) and 3.10 fall back to tomli
    import tomli as tomllib
import zipfile

import pytest

from pytrain_grader import workspace


def read_pyproject():
    path = workspace() / "pyproject.toml"
    if not path.exists():
        pytest.fail("pyproject.toml not found in your workspace")
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        pytest.fail(f"pyproject.toml is not valid TOML: {e}")


def project_table():
    data = read_pyproject()
    if "project" not in data:
        pytest.fail("pyproject.toml needs a [project] table")
    return data["project"]


def test_name_and_version():
    proj = project_table()
    assert proj.get("name") == "greet"
    assert proj.get("version") == "0.1.0"


def test_description_and_requires_python():
    from packaging.specifiers import SpecifierSet

    proj = project_table()
    assert str(proj.get("description", "")).strip(), "description must be non-empty"
    rp = proj.get("requires-python")
    assert rp, "requires-python is missing"
    spec = SpecifierSet(rp)
    assert spec.contains("3.12"), "requires-python should allow modern pythons like 3.12"
    assert not spec.contains("3.8"), "requires-python should rule out pythons below 3.11"


def test_dependencies_declared():
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    proj = project_table()
    reqs = {}
    for raw in proj.get("dependencies", []):
        r = Requirement(raw)
        reqs[canonicalize_name(r.name)] = r
    assert "colorama" in reqs, "declare colorama as a runtime dependency"
    assert "packaging" in reqs, "declare packaging as a runtime dependency"
    spec = reqs["colorama"].specifier
    assert spec.contains("0.4.6"), "the colorama constraint should allow 0.4.6"
    assert not spec.contains("0.3"), "colorama must require at least 0.4 (0.3 should be excluded)"


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
        pytest.fail("build succeeded but produced no wheel")
    return wheels[0]


def test_wheel_contains_the_module(wheel):
    with zipfile.ZipFile(wheel) as z:
        names = z.namelist()
    assert "greet.py" in names, f"greet.py is missing from the wheel (contents: {names})"


def test_wheel_metadata(wheel):
    with zipfile.ZipFile(wheel) as z:
        meta_files = [n for n in z.namelist() if n.endswith(".dist-info/METADATA")]
        assert meta_files, "wheel has no METADATA file"
        meta = z.read(meta_files[0]).decode()
    assert "Name: greet" in meta
    assert "Version: 0.1.0" in meta
    requires = "\n".join(
        line for line in meta.splitlines() if line.startswith("Requires-Dist:")
    ).lower()
    assert "colorama" in requires, "colorama did not make it into the built metadata"
    assert "packaging" in requires, "packaging did not make it into the built metadata"
