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


def run_py(installed, code):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(installed)
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, env=env, cwd=str(installed),
    )


def test_flat_module_is_gone():
    assert not (workspace() / "textstats.py").exists(), \
        "delete the flat textstats.py — the code must live in src/textstats/"


def test_src_package_structure():
    assert (workspace() / "src" / "textstats" / "__init__.py").exists(), \
        "expected src/textstats/__init__.py"
    assert (workspace() / "src" / "textstats" / "stats.py").exists(), \
        "expected the implementations in src/textstats/stats.py"


def test_installed_public_api(installed):
    code = (
        "from textstats import word_count, unique_words, top_words\n"
        "text = 'the cat and the dog and the bird'\n"
        "print(word_count(text))\n"
        "print(','.join(unique_words(text)))\n"
        "print(top_words(text, 2))\n"
    )
    proc = run_py(installed, code)
    assert proc.returncode == 0, f"importing the installed textstats failed:\n{proc.stderr}"
    lines = proc.stdout.strip().splitlines()
    assert lines[0] == "8"
    assert lines[1] == "and,bird,cat,dog,the"
    assert lines[2] == "[('the', 3), ('and', 2)]"


def test_installed_submodule(installed):
    proc = run_py(
        installed,
        "from textstats.stats import top_words; print(top_words('a b a', 1))",
    )
    assert proc.returncode == 0, f"textstats.stats is not importable when installed:\n{proc.stderr}"
    assert proc.stdout.strip() == "[('a', 2)]"


def test_edge_behaviour_preserved(installed):
    proc = run_py(
        installed,
        "from textstats import word_count, unique_words; "
        "print(word_count('')); print(unique_words(''))",
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip().splitlines() == ["0", "[]"]
