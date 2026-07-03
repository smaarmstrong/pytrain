import subprocess
import sys
import typing

from pytrain_grader import load_solution, get_attr, workspace


def _mypy(target):
    return subprocess.run(
        [sys.executable, "-m", "mypy", "--no-error-summary", "--soft-error-limit=-1",
         "--disallow-untyped-defs", str(target)],
        capture_output=True, text=True, cwd=str(workspace()),
    )


# ---- structure --------------------------------------------------------------

def test_typeddicts_defined_with_right_keys():
    mod = load_solution()
    Address = get_attr(mod, "Address")
    UserProfile = get_attr(mod, "UserProfile")
    assert typing.is_typeddict(Address), "Address must be a TypedDict"
    assert typing.is_typeddict(UserProfile), "UserProfile must be a TypedDict"
    assert Address.__required_keys__ == {"street", "city"}
    assert UserProfile.__required_keys__ == {"name", "age", "address"}, (
        "name/age/address must be required keys"
    )
    assert UserProfile.__optional_keys__ == {"nickname"}, (
        "nickname must be the (only) NotRequired key"
    )
    hints = typing.get_type_hints(UserProfile)
    assert hints["address"] is Address, "address must be the nested Address TypedDict"


# ---- behaviour --------------------------------------------------------------

def test_make_profile_without_nickname_omits_key():
    f = get_attr(load_solution(), "make_profile")
    p = f("Ada", 36, "1 Duke St", "London")
    assert p == {"name": "Ada", "age": 36,
                 "address": {"street": "1 Duke St", "city": "London"}}
    assert "nickname" not in p


def test_make_profile_with_nickname():
    f = get_attr(load_solution(), "make_profile")
    p = f("Ada", 36, "1 Duke St", "London", nickname="Countess")
    assert p["nickname"] == "Countess"
    assert p["address"] == {"street": "1 Duke St", "city": "London"}


def test_describe_both_shapes():
    mod = load_solution()
    make, describe = get_attr(mod, "make_profile"), get_attr(mod, "describe")
    assert describe(make("Ada", 36, "1 Duke St", "London")) == "Ada (36) of London"
    assert describe(make("Ada", 36, "1 Duke St", "London", nickname="Countess")) \
        == "Ada (36) of London, aka Countess"


# ---- typing -----------------------------------------------------------------

def test_mypy_clean_on_module():
    proc = _mypy(workspace() / "solution.py")
    assert proc.returncode == 0, (
        "mypy is not clean under --disallow-untyped-defs:\n" + proc.stdout + proc.stderr
    )


def test_mypy_accepts_valid_profiles():
    snippet = workspace() / "_check_td_ok.py"
    snippet.write_text(
        "from solution import Address, UserProfile\n"
        'addr: Address = {"street": "1 Duke St", "city": "London"}\n'
        'p1: UserProfile = {"name": "Ada", "age": 36, "address": addr}\n'
        'p2: UserProfile = {"name": "Ada", "age": 36, "address": addr,\n'
        '                   "nickname": "Countess"}\n'
    )
    proc = _mypy(snippet)
    assert proc.returncode == 0, (
        "mypy rejected valid UserProfile values (is nickname NotRequired?):\n"
        + proc.stdout + proc.stderr
    )


def test_mypy_rejects_profile_missing_required_key():
    snippet = workspace() / "_check_td_bad.py"
    snippet.write_text(
        "from solution import UserProfile\n"
        'p: UserProfile = {"name": "Ada", "age": 36}  # no address\n'
    )
    proc = _mypy(snippet)
    assert proc.returncode != 0, (
        "mypy accepted a UserProfile with no 'address' — is address required?"
    )
