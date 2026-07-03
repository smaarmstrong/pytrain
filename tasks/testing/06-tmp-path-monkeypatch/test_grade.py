"""Meta-grader: the learner's suite must exercise real files (tmp_path) and
the process environment (monkeypatch) — each bad implementation is only
distinguishable through one of those."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_confload.py"
TARGET_FILE = "confload.py"

GOOD = '''\
import json
import os


def save_config(path, cfg):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f)


def load_config(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_setting(name, default=None):
    raw = os.environ.get("APP_" + name.upper())
    if raw is None:
        return default
    low = raw.lower()
    if low in ("true", "false"):
        return low == "true"
    if raw.isdigit():
        return int(raw)
    return raw
'''


def _mutant(old, new):
    src = GOOD.replace(old, new)
    assert src != GOOD, f"mutant substitution failed: {old!r}"
    return src


BADS = {
    "missing_file_raises": _mutant(
        '    if not os.path.exists(path):\n        return {}\n',
        "",
    ),
    "saves_values_as_strings": _mutant(
        "        json.dump(cfg, f)",
        "        json.dump({k: str(v) for k, v in cfg.items()}, f)",
    ),
    "ignores_environment": _mutant(
        '    raw = os.environ.get("APP_" + name.upper())',
        "    raw = None",
    ),
    "forgets_to_uppercase_name": _mutant(
        '    raw = os.environ.get("APP_" + name.upper())',
        '    raw = os.environ.get("APP_" + name)',
    ),
    "bools_stay_strings": _mutant(
        '    low = raw.lower()\n    if low in ("true", "false"):\n        return low == "true"\n',
        "",
    ),
    "digits_stay_strings": _mutant(
        "    if raw.isdigit():\n        return int(raw)\n",
        "",
    ),
}


def run_learner_tests(impl_src, tmp_path, extra=()):
    learner = workspace() / TEST_FILE
    if not learner.exists():
        pytest.fail(f"{TEST_FILE} not found in your workspace")
    (tmp_path / TARGET_FILE).write_text(impl_src)
    (tmp_path / TEST_FILE).write_text(learner.read_text())
    env = os.environ.copy()
    env.pop("PYTEST_ADDOPTS", None)
    env.pop("PYTEST_PLUGINS", None)
    # make sure no APP_* variable leaks into the learner's test run
    for key in [k for k in env if k.startswith("APP_")]:
        env.pop(key)
    env["PYTHONPATH"] = str(tmp_path)
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(tmp_path), "-q",
         "-p", "no:cacheprovider", *extra],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=90,
    )


def tail(proc):
    return (proc.stdout + proc.stderr)[-1500:]


def test_your_tests_pass_a_correct_implementation(tmp_path):
    proc = run_learner_tests(GOOD, tmp_path)
    assert proc.returncode == 0, (
        "your tests must all PASS against a correct implementation, but:\n" + tail(proc)
    )


@pytest.mark.parametrize("bug", sorted(BADS))
def test_your_tests_catch_each_bug(bug, tmp_path):
    proc = run_learner_tests(BADS[bug], tmp_path)
    if proc.returncode == 0:
        pytest.fail(f"a buggy implementation ({bug.replace('_', ' ')}) passed your "
                    "tests — add a test that catches it (see the spec)")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against the '{bug}' "
                    f"implementation:\n{tail(proc)}")
