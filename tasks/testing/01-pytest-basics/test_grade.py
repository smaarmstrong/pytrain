"""Meta-grader: runs the learner's test_slugify.py against a known-good
implementation (must PASS) and several known-bad ones (must FAIL each)."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_slugify.py"
TARGET_FILE = "slugify.py"

GOOD = '''\
import re


def slugify(text):
    text = text.lower()
    text = re.sub(r"[ _]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")
'''

BADS = {
    "does_not_lowercase": '''\
import re


def slugify(text):
    text = re.sub(r"[ _]+", "-", text)
    text = re.sub(r"[^a-zA-Z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")
''',
    "deletes_underscores_instead_of_hyphenating": '''\
import re


def slugify(text):
    text = text.lower()
    text = re.sub(r" +", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")
''',
    "does_not_collapse_hyphen_runs": '''\
import re


def slugify(text):
    text = text.lower()
    text = re.sub(r"[ _]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    return text.strip("-")
''',
    "keeps_leading_trailing_hyphens": '''\
import re


def slugify(text):
    text = text.lower()
    text = re.sub(r"[ _]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text
''',
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
