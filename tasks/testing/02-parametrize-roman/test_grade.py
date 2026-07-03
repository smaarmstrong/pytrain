"""Meta-grader: the learner's parametrized suite must discriminate good from
buggy roman-numeral implementations, expose the required test ids, and mark
the boundary cases."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_roman.py"
TARGET_FILE = "roman.py"

GOOD = '''\
_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n):
    if not 1 <= n <= 3999:
        raise ValueError(f"expected 1..3999, got {n}")
    out = []
    for value, symbol in _VALUES:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)
'''

_BAD_TEMPLATE = '''\
_VALUES = [
%s
]


def to_roman(n):
    if not 1 <= n <= 3999:
        raise ValueError(f"expected 1..3999, got {n}")
    out = []
    for value, symbol in _VALUES:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)
'''

BADS = {
    # 4 -> "IIII", 9 -> "VIIII"
    "no_subtractive_units": _BAD_TEMPLATE % (
        '    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),\n'
        '    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),\n'
        '    (10, "X"), (5, "V"), (1, "I"),'
    ),
    # 40 -> "XXXX", 90 -> "LXXXX"
    "no_subtractive_tens": _BAD_TEMPLATE % (
        '    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),\n'
        '    (100, "C"), (50, "L"),\n'
        '    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),'
    ),
    # 900 -> "DCCCC", 400 -> "CCCC" (breaks 1994)
    "no_subtractive_hundreds": _BAD_TEMPLATE % (
        '    (1000, "M"), (500, "D"),\n'
        '    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),\n'
        '    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),'
    ),
    "accepts_out_of_range": '''\
_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n):
    out = []
    for value, symbol in _VALUES:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)
''',
}

REQUIRED_IDS = ["one", "four", "nine", "forty", "ninety", "mcmxciv", "max"]


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


def collected_ids(proc):
    return [line for line in proc.stdout.splitlines() if "::" in line]


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
                    "tests — add/extend a parametrized case that catches it")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against the '{bug}' "
                    f"implementation:\n{tail(proc)}")


def test_required_parametrize_ids_exist(tmp_path):
    proc = run_learner_tests(GOOD, tmp_path, extra=("--collect-only",))
    missing = [i for i in REQUIRED_IDS if f"[{i}]" not in proc.stdout]
    assert not missing, (
        f"these required test ids are missing: {missing} — "
        "use pytest.param(..., id=...) as shown in the prompt"
    )


def test_boundary_mark_selects_only_the_boundaries(tmp_path):
    proc_all = run_learner_tests(GOOD, tmp_path, extra=("--collect-only",))
    proc_boundary = run_learner_tests(GOOD, tmp_path,
                                      extra=("--collect-only", "-m", "boundary"))
    everything = collected_ids(proc_all)
    selected = collected_ids(proc_boundary)
    assert any("[one]" in line for line in selected), \
        "the `one` case must carry pytest.mark.boundary"
    assert any("[max]" in line for line in selected), \
        "the `max` case must carry pytest.mark.boundary"
    assert len(selected) < len(everything), \
        "-m boundary must select a strict subset — don't mark every case"
