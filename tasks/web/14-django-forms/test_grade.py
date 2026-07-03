"""Django forms grader — module loaded once and cached (app-registry safety)."""
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="pytrain-test-key",
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
        USE_TZ=True,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

import pytest  # noqa: E402

from pytrain_grader import load_solution, get_attr  # noqa: E402

_cache = {}


def form_cls():
    if "mod" not in _cache:
        _cache["mod"] = load_solution()
    return get_attr(_cache["mod"], "SignupForm")


def data(**overrides):
    base = {
        "username": "Ada99",
        "email": "ada@example.com",
        "age": "36",
        "password": "s3cret-pw",
        "password2": "s3cret-pw",
    }
    base.update(overrides)
    return base


def test_valid_form():
    form = form_cls()(data())
    assert form.is_valid(), form.errors
    assert form.cleaned_data["age"] == 36


def test_username_lowercased():
    form = form_cls()(data(username="AdaLovelace"))
    assert form.is_valid(), form.errors
    assert form.cleaned_data["username"] == "adalovelace"


def test_username_too_short():
    form = form_cls()(data(username="ab"))
    assert not form.is_valid()
    assert "username" in form.errors


def test_username_too_long():
    form = form_cls()(data(username="a" * 21))
    assert not form.is_valid()
    assert "username" in form.errors


def test_username_non_alnum_message():
    form = form_cls()(data(username="ada lovelace"))
    assert not form.is_valid()
    assert "letters and digits only" in str(form.errors["username"])
    form = form_cls()(data(username="ada-99"))
    assert not form.is_valid()
    assert "letters and digits only" in str(form.errors["username"])


def test_bad_email():
    form = form_cls()(data(email="not-an-email"))
    assert not form.is_valid()
    assert "email" in form.errors


def test_age_below_13():
    form = form_cls()(data(age="12"))
    assert not form.is_valid()
    assert "age" in form.errors


def test_age_13_ok():
    assert form_cls()(data(age="13")).is_valid()


def test_age_not_a_number():
    form = form_cls()(data(age="old"))
    assert not form.is_valid()
    assert "age" in form.errors


def test_short_password():
    form = form_cls()(data(password="short", password2="short"))
    assert not form.is_valid()
    assert "password" in form.errors


def test_password_mismatch_is_non_field_error():
    form = form_cls()(data(password="aaaaaaaa", password2="bbbbbbbb"))
    assert not form.is_valid()
    assert any("passwords do not match" in e for e in form.non_field_errors())
    assert "username" not in form.errors  # other fields still fine


def test_matching_passwords_no_error():
    form = form_cls()(data(password="aaaaaaaa", password2="aaaaaaaa"))
    assert form.is_valid(), form.errors


def test_all_fields_required():
    form = form_cls()({})
    assert not form.is_valid()
    for field in ("username", "email", "age", "password", "password2"):
        assert field in form.errors, f"missing required error for {field}"
