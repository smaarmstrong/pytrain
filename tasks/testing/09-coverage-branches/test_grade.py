"""Meta-grader: seven mutants, each breaking exactly one branch of quote().
The learner's suite must pass the good implementation and kill every mutant."""
import os
import subprocess
import sys

import pytest

from pytrain_grader import workspace

TEST_FILE = "test_shipping.py"
TARGET_FILE = "shipping.py"

GOOD = '''\
def quote(weight, zone, express=False, member=False):
    if weight <= 0:                                    # B1
        raise ValueError("weight must be positive")
    if zone not in ("A", "B", "C"):                    # B2
        raise ValueError(f"unknown zone: {zone}")
    base = {"A": 5.0, "B": 8.0, "C": 12.0}[zone]
    if weight > 20:                                    # B3: heavy tier
        cost = base + 20 * 0.5 + (weight - 20) * 0.25
    else:                                              # B4: light tier
        cost = base + weight * 0.5
    if express:                                        # B5: express multiplier
        cost *= 1.75
        if zone == "C":                                # B6: remote surcharge
            cost += 10.0
    if member:                                         # B7: capped discount
        cost -= min(5.0, cost * 0.1)
    return round(cost, 2)
'''


def _mutant(*pairs):
    src = GOOD
    for old, new in pairs:
        replaced = src.replace(old, new)
        assert replaced != src, f"mutant substitution failed: {old!r}"
        src = replaced
    return src


MUTANTS = {
    "b1_accepts_nonpositive_weight": _mutant(
        ("    if weight <= 0:", "    if False:"),
    ),
    "b2_unknown_zone_treated_as_a": _mutant(
        ('    if zone not in ("A", "B", "C"):', "    if False:"),
        ('}[zone]', '}.get(zone, 5.0)'),
    ),
    "b3_heavy_tier_ignored": _mutant(
        ("    cost = base + 20 * 0.5 + (weight - 20) * 0.25",
         "    cost = base + weight * 0.5"),
    ),
    "b4_light_rate_wrong": _mutant(
        ("        cost = base + weight * 0.5", "        cost = base + weight * 0.45"),
    ),
    "b5_express_multiplier_wrong": _mutant(
        ("        cost *= 1.75", "        cost *= 1.5"),
    ),
    "b6_no_remote_surcharge": _mutant(
        ("            cost += 10.0", "            pass"),
    ),
    "b7_discount_uncapped": _mutant(
        ("        cost -= min(5.0, cost * 0.1)", "        cost -= cost * 0.1"),
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
    env["PYTHONPATH"] = str(tmp_path)
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(tmp_path), "-q",
         "-p", "no:cacheprovider", *extra],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=90,
    )


def tail(proc):
    return (proc.stdout + proc.stderr)[-1500:]


def test_your_tests_pass_the_correct_implementation(tmp_path):
    proc = run_learner_tests(GOOD, tmp_path)
    assert proc.returncode == 0, (
        "your tests must all PASS against the correct implementation, but:\n" + tail(proc)
    )


@pytest.mark.parametrize("mutant", sorted(MUTANTS))
def test_your_tests_kill_each_mutant(mutant, tmp_path):
    proc = run_learner_tests(MUTANTS[mutant], tmp_path)
    if proc.returncode == 0:
        pytest.fail(f"mutant '{mutant}' survived your suite — the branch it breaks "
                    "is not really tested")
    if proc.returncode != 1:
        pytest.fail(f"your tests did not run cleanly against mutant '{mutant}':\n"
                    + tail(proc))
