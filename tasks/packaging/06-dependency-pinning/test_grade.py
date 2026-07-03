import pytest

from pytrain_grader import workspace

SPANNER = ["1.0", "1.4", "1.5", "1.7.2", "2.0", "2.1"]
GEARBOX = ["0.9", "1.5", "1.6", "2.0"]


def parse_constraints():
    from packaging.requirements import InvalidRequirement, Requirement
    from packaging.utils import canonicalize_name

    path = workspace() / "constraints.txt"
    if not path.exists():
        pytest.fail("constraints.txt not found in your workspace")
    reqs = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            r = Requirement(line)
        except InvalidRequirement as e:
            pytest.fail(f"constraints.txt line {lineno} is not a valid requirement: {line!r} ({e})")
        reqs[canonicalize_name(r.name)] = r
    if not reqs:
        pytest.fail("constraints.txt has no requirement lines yet")
    return reqs


def allowed(req, versions):
    return [v for v in versions if req.specifier.contains(v)]


def test_both_packages_constrained():
    reqs = parse_constraints()
    assert "spanner" in reqs, "add a constraint line for spanner"
    assert "gearbox" in reqs, "add a constraint line for gearbox"


def test_spanner_constraint():
    reqs = parse_constraints()
    if "spanner" not in reqs:
        pytest.fail("add a constraint line for spanner")
    ok = allowed(reqs["spanner"], SPANNER)
    assert ok, "your spanner constraint admits none of the published versions"
    for bad in ("1.0", "1.4"):
        assert bad not in ok, f"spanner {bad} lacks the feature your app needs (added in 1.5)"
    for bad in ("2.0", "2.1"):
        assert bad not in ok, f"spanner {bad} breaks gearbox 1.5+ (they require spanner < 2)"


def test_gearbox_constraint():
    reqs = parse_constraints()
    if "gearbox" not in reqs:
        pytest.fail("add a constraint line for gearbox")
    ok = allowed(reqs["gearbox"], GEARBOX)
    assert ok, "your gearbox constraint admits none of the published versions"
    assert "0.9" not in ok, "your app needs gearbox >= 1.5"
    assert "2.0" not in ok, "gearbox 2.0 has the critical bug — it must be excluded"


def test_a_real_resolution_exists():
    reqs = parse_constraints()
    if "spanner" not in reqs or "gearbox" not in reqs:
        pytest.fail("constrain both spanner and gearbox")
    pairs = [
        (s, g)
        for s in allowed(reqs["spanner"], SPANNER)
        for g in allowed(reqs["gearbox"], GEARBOX)
    ]
    assert pairs, "no (spanner, gearbox) version pair satisfies your constraints"
