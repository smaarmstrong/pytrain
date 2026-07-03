"""Django views grader — module loaded once and cached (app-registry safety)."""
import json

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
from django.test import Client  # noqa: E402
from django.test.utils import override_settings  # noqa: E402

from pytrain_grader import load_solution  # noqa: E402

_cache = {}


def _mod():
    if "mod" not in _cache:
        _cache["mod"] = load_solution()
    return _cache["mod"]


@pytest.fixture()
def client():
    with override_settings(ROOT_URLCONF=_mod()):
        yield Client()


def test_ping(client):
    r = client.get("/ping/")
    assert r.status_code == 200
    assert json.loads(r.content) == {"pong": True}


def test_square(client):
    r = client.get("/square/7/")
    assert r.status_code == 200
    assert json.loads(r.content) == {"result": 49}
    assert json.loads(client.get("/square/0/").content) == {"result": 0}


def test_square_non_int_is_404(client):
    assert client.get("/square/notanumber/").status_code == 404


def test_add(client):
    r = client.get("/add/", {"a": 2, "b": 40})
    assert r.status_code == 200
    assert json.loads(r.content) == {"sum": 42}


def test_add_negative(client):
    r = client.get("/add/", {"a": -5, "b": 3})
    assert json.loads(r.content) == {"sum": -2}


def test_add_missing_param_400(client):
    r = client.get("/add/", {"a": 2})
    assert r.status_code == 400
    assert json.loads(r.content) == {"error": "a and b must be integers"}


def test_add_non_int_400(client):
    r = client.get("/add/", {"a": 2, "b": "fish"})
    assert r.status_code == 400
    assert json.loads(r.content) == {"error": "a and b must be integers"}


def test_echo_roundtrip(client):
    payload = {"x": [1, 2], "nested": {"ok": True}}
    r = client.post("/echo/", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 200
    assert json.loads(r.content) == {"you_sent": payload}


def test_echo_invalid_json_400(client):
    r = client.post("/echo/", data="{not json", content_type="application/json")
    assert r.status_code == 400
    assert json.loads(r.content) == {"error": "invalid json"}


def test_echo_wrong_method_405(client):
    assert client.get("/echo/").status_code == 405
    assert client.put("/echo/", data="{}", content_type="application/json").status_code == 405


def test_unknown_url_404(client):
    assert client.get("/nope/").status_code == 404
