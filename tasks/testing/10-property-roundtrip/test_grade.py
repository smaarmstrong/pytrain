"""Meta-grader: the buggy codecs only misbehave on input classes that a
seeded random sweep hits with near-certainty (runs >= 10, trailing singles,
empty strings, unmerged runs) — hand-picked examples rarely do."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_codec.py"
TARGET_FILE = "codec.py"

GOOD = '''\
def encode(s):
    pairs = []
    for ch in s:
        if pairs and pairs[-1][0] == ch:
            pairs[-1] = (ch, pairs[-1][1] + 1)
        else:
            pairs.append((ch, 1))
    return pairs


def decode(pairs):
    return "".join(ch * count for ch, count in pairs)
'''

BADS = {
    # splits runs at length 9: round-trips fine, violates "maximal runs"
    # only when a run of 10+ occurs
    "splits_runs_longer_than_nine": '''\
def encode(s):
    pairs = []
    for ch in s:
        if pairs and pairs[-1][0] == ch and pairs[-1][1] < 9:
            pairs[-1] = (ch, pairs[-1][1] + 1)
        else:
            pairs.append((ch, 1))
    return pairs


def decode(pairs):
    return "".join(ch * count for ch, count in pairs)
''',
    # drops the final pair when it is a single character
    "drops_trailing_single": '''\
def encode(s):
    pairs = []
    for ch in s:
        if pairs and pairs[-1][0] == ch:
            pairs[-1] = (ch, pairs[-1][1] + 1)
        else:
            pairs.append((ch, 1))
    if pairs and pairs[-1][1] == 1:
        pairs.pop()
    return pairs


def decode(pairs):
    return "".join(ch * count for ch, count in pairs)
''',
    # returns a zero-count pair for "": round-trips fine, violates count >= 1
    "zero_count_pair_for_empty": '''\
def encode(s):
    if not s:
        return [("", 0)]
    pairs = []
    for ch in s:
        if pairs and pairs[-1][0] == ch:
            pairs[-1] = (ch, pairs[-1][1] + 1)
        else:
            pairs.append((ch, 1))
    return pairs


def decode(pairs):
    return "".join(ch * count for ch, count in pairs)
''',
    # never merges: round-trips fine, violates "maximal runs" whenever any
    # run of 2+ occurs
    "never_merges_runs": '''\
def encode(s):
    return [(ch, 1) for ch in s]


def decode(pairs):
    return "".join(ch * count for ch, count in pairs)
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
                    "tests — the seeded random sweep from the prompt would catch it")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against the '{bug}' "
                    f"implementation:\n{tail(proc)}")
