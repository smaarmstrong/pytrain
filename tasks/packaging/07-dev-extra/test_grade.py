import subprocess
import sys
import tomllib
import zipfile

import pytest

from pytrain_grader import workspace


def project_table():
    path = workspace() / "pyproject.toml"
    if not path.exists():
        pytest.fail("pyproject.toml not found in your workspace")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        pytest.fail(f"pyproject.toml is not valid TOML: {e}")
    return data.get("project", {})


def test_dev_extra_declared():
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    extras = project_table().get("optional-dependencies", {})
    assert "dev" in extras, "declare a `dev` extra under [project.optional-dependencies]"
    names = {canonicalize_name(Requirement(r).name) for r in extras["dev"]}
    assert "pytest" in names, "the dev extra must include pytest"


def test_pytest_is_not_a_runtime_dep():
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    deps = project_table().get("dependencies", [])
    names = {canonicalize_name(Requirement(r).name) for r in deps}
    assert "pytest" not in names, \
        "pytest belongs in the dev extra, not in the runtime dependencies"


@pytest.fixture(scope="session")
def metadata(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    proc = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation",
         "--outdir", str(out), str(workspace())],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.fail("`python -m build --wheel` failed:\n" + (proc.stdout + proc.stderr)[-2000:])
    whl = next(iter(out.glob("*.whl")))
    with zipfile.ZipFile(whl) as z:
        name = [n for n in z.namelist() if n.endswith(".dist-info/METADATA")][0]
        return z.read(name).decode()


def test_built_metadata_provides_the_extra(metadata):
    assert "Provides-Extra: dev" in metadata, \
        "the built wheel metadata does not declare the dev extra"


def test_pytest_requirement_is_gated_by_the_extra(metadata):
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    reqs = [
        Requirement(line.split(":", 1)[1].strip())
        for line in metadata.splitlines()
        if line.startswith("Requires-Dist:")
    ]
    pytest_reqs = [r for r in reqs if canonicalize_name(r.name) == "pytest"]
    assert pytest_reqs, "the built metadata has no Requires-Dist entry for pytest"
    for r in pytest_reqs:
        assert r.marker is not None, \
            "pytest is an unconditional dependency — it must be gated behind the dev extra"
        assert r.marker.evaluate({"extra": "dev"}) is True, \
            "installing with the dev extra should pull in pytest"
        assert r.marker.evaluate({"extra": ""}) is False, \
            "a plain install (no extras) must NOT pull in pytest"
