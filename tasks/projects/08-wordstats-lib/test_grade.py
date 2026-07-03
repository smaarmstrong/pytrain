"""Grades the packaging end-to-end, all offline:

    workspace --[python -m build --no-isolation --wheel]--> wheel
    wheel --[pip install --no-index --no-deps --target]--> scratch site dir
    grade the INSTALLED package + the INSTALLED console script.

No index access, no venv mutation, no ports.
"""
import importlib
import importlib.metadata
import os
import subprocess
import sys
from pathlib import Path

import pytest

from pytrain_grader import workspace

SAMPLE = "the cat sat on the mat\nThe dog and the cat\n"


def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=180, **kw)


def _tail(proc):
    out = (proc.stdout or "") + (proc.stderr or "")
    return "\n".join(out.strip().splitlines()[-8:])


@pytest.fixture(scope="session")
def installed(tmp_path_factory):
    """Build the wheel from the workspace and pip-install it into a scratch dir."""
    ws = workspace()
    dist = tmp_path_factory.mktemp("dist")
    proc = _run([sys.executable, "-m", "build", "--no-isolation", "--wheel",
                 "--outdir", str(dist)], cwd=str(ws))
    if proc.returncode != 0:
        pytest.fail("`python -m build --no-isolation --wheel` failed — fix "
                    "pyproject.toml first:\n" + _tail(proc))
    wheels = sorted(dist.glob("*.whl"))
    if len(wheels) != 1:
        pytest.fail(f"expected exactly one wheel in dist/, got {[w.name for w in wheels]}")
    wheel = wheels[0]
    if not wheel.name.startswith("wordstats-0.1.0-"):
        pytest.fail(f"wheel is named {wheel.name!r} — project must be "
                    "`wordstats` version `0.1.0`")

    target = tmp_path_factory.mktemp("site")
    proc = _run([sys.executable, "-m", "pip", "install", "--no-index", "--no-deps",
                 "--quiet", "--target", str(target), str(wheel)])
    if proc.returncode != 0:
        pytest.fail("pip could not install the built wheel:\n" + _tail(proc))
    return target


@pytest.fixture(scope="session")
def pkg(installed):
    """Import the installed package (never the workspace src/ tree)."""
    sys.path.insert(0, str(installed))
    for name in [n for n in sys.modules if n == "wordstats" or n.startswith("wordstats.")]:
        del sys.modules[name]
    mod = importlib.import_module("wordstats")
    assert str(installed) in str(Path(mod.__file__).resolve()), \
        "imported wordstats from the wrong place (packaging is broken)"
    return mod


def run_cli(installed, *args):
    script = None
    for sub in ("bin", "Scripts"):
        cand = installed / sub / "wordstats"
        if cand.exists():
            script = cand
            break
        if cand.with_suffix(".exe").exists():
            script = cand.with_suffix(".exe")
            break
    if script is None:
        pytest.fail("no `wordstats` console script was installed — declare it "
                    "under [project.scripts] in pyproject.toml")
    env = dict(os.environ, PYTHONPATH=str(installed))
    return _run([sys.executable, str(script), *args], env=env)


# -- metadata + entry point ---------------------------------------------------

def test_version_metadata_and_attribute(pkg, installed):
    (dist,) = importlib.metadata.Distribution.discover(
        name="wordstats", path=[str(installed)])
    assert dist.version == "0.1.0"
    assert pkg.__version__ == "0.1.0"


def test_console_script_entry_point_declared_and_resolvable(pkg, installed):
    (dist,) = importlib.metadata.Distribution.discover(
        name="wordstats", path=[str(installed)])
    eps = [ep for ep in dist.entry_points
           if ep.group == "console_scripts" and ep.name == "wordstats"]
    assert eps, "no console_scripts entry point named `wordstats` in the wheel"
    modname, _, attr = eps[0].value.partition(":")
    fn = getattr(importlib.import_module(modname), attr.split(".")[0])
    assert callable(fn)


# -- library API (the installed package) --------------------------------------

def test_count_words_lowercases_and_splits_on_punctuation(pkg):
    assert pkg.count_words("Don't stop, DON'T stop!") == {"don't": 2, "stop": 2}
    assert pkg.count_words("a2b c a2b") == {"a2b": 2, "c": 1}


def test_count_words_empty(pkg):
    assert pkg.count_words("") == {}


def test_top_words_orders_count_desc_then_alpha(pkg):
    text = "b a b a c c c d"
    assert pkg.top_words(text, 3) == [("c", 3), ("a", 2), ("b", 2)]
    assert pkg.top_words("x", 10) == [("x", 1)]      # n may exceed vocabulary


def test_top_words_default_n_is_5(pkg):
    text = "a a a b b c d e f"                       # 6 unique words
    got = pkg.top_words(text)
    assert got == [("a", 3), ("b", 2), ("c", 1), ("d", 1), ("e", 1)]


def test_summarise(pkg):
    assert pkg.summarise(SAMPLE) == {"lines": 2, "words": 11, "unique": 7}
    assert pkg.summarise("") == {"lines": 0, "words": 0, "unique": 0}


# -- the installed CLI ---------------------------------------------------------

def test_cli_default_top_3(pkg, installed, tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text(SAMPLE, encoding="utf-8")
    proc = run_cli(installed, str(f))
    assert proc.returncode == 0, proc.stderr
    lines = [l.strip() for l in proc.stdout.strip().splitlines()]
    assert lines == ["lines=2 words=11 unique=7", "the 4", "cat 2", "and 1"]


def test_cli_respects_top_option(pkg, installed, tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text(SAMPLE, encoding="utf-8")
    proc = run_cli(installed, str(f), "--top", "2")
    assert proc.returncode == 0, proc.stderr
    lines = [l.strip() for l in proc.stdout.strip().splitlines()]
    assert lines == ["lines=2 words=11 unique=7", "the 4", "cat 2"]


def test_cli_missing_file_exits_2_with_stderr(pkg, installed, tmp_path):
    ghost = tmp_path / "no-such-file.txt"
    proc = run_cli(installed, str(ghost))
    assert proc.returncode == 2
    assert str(ghost) in proc.stderr
    assert proc.stdout.strip() == ""
