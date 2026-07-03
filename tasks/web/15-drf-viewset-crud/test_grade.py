"""DRF grader — learner module loaded once and cached (app-registry safety)."""
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="pytrain-test-key",
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "rest_framework",
        ],
        USE_TZ=True,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

import pytest  # noqa: E402
from django.test.utils import override_settings  # noqa: E402
from rest_framework.test import APIClient  # noqa: E402

from pytrain_grader import load_solution, get_attr  # noqa: E402

_cache = {}


def _mod():
    if "mod" not in _cache:
        mod = load_solution()
        _cache["mod"] = mod
        from django.db import connection

        snippet = get_attr(mod, "Snippet")
        with connection.schema_editor() as se:
            se.create_model(snippet)
    return _cache["mod"]


@pytest.fixture()
def mod():
    m = _mod()
    get_attr(m, "Snippet").objects.all().delete()
    return m


@pytest.fixture()
def client(mod):
    with override_settings(ROOT_URLCONF=mod):
        yield APIClient()


def make(client, title="hello", code="print('hi')", language=None):
    body = {"title": title, "code": code}
    if language is not None:
        body["language"] = language
    return client.post("/snippets/", body, format="json")


def test_create_201_with_default_language(client):
    r = make(client)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "hello"
    assert body["code"] == "print('hi')"
    assert body["language"] == "python"
    assert isinstance(body["id"], int)


def test_create_explicit_language(client):
    r = make(client, language="rust")
    assert r.status_code == 201
    assert r.json()["language"] == "rust"


def test_create_missing_title_400(client):
    r = client.post("/snippets/", {"code": "no title"}, format="json")
    assert r.status_code == 400
    assert "title" in r.json()


def test_create_missing_code_400(client):
    r = client.post("/snippets/", {"title": "no code"}, format="json")
    assert r.status_code == 400


def test_list_ordered_by_id(client):
    make(client, title="a")
    make(client, title="b")
    make(client, title="c")
    r = client.get("/snippets/")
    assert r.status_code == 200
    got = r.json()
    assert [s["title"] for s in got] == ["a", "b", "c"]
    ids = [s["id"] for s in got]
    assert ids == sorted(ids)


def test_serializer_fields_exact(client):
    make(client)
    (snippet,) = client.get("/snippets/").json()
    assert set(snippet.keys()) == {"id", "title", "code", "language"}


def test_retrieve(client):
    sid = make(client, title="findme").json()["id"]
    r = client.get(f"/snippets/{sid}/")
    assert r.status_code == 200
    assert r.json()["title"] == "findme"


def test_retrieve_missing_404(client):
    assert client.get("/snippets/99999/").status_code == 404


def test_put_replaces(client):
    sid = make(client).json()["id"]
    r = client.put(
        f"/snippets/{sid}/",
        {"title": "new", "code": "pass", "language": "go"},
        format="json",
    )
    assert r.status_code == 200
    assert r.json() == {"id": sid, "title": "new", "code": "pass", "language": "go"}


def test_put_missing_title_400(client):
    sid = make(client).json()["id"]
    r = client.put(f"/snippets/{sid}/", {"code": "pass"}, format="json")
    assert r.status_code == 400


def test_patch_partial(client):
    sid = make(client, title="keep", code="keep()").json()["id"]
    r = client.patch(f"/snippets/{sid}/", {"language": "rust"}, format="json")
    assert r.status_code == 200
    assert r.json() == {"id": sid, "title": "keep", "code": "keep()", "language": "rust"}


def test_delete_204_then_404(client, mod):
    sid = make(client).json()["id"]
    r = client.delete(f"/snippets/{sid}/")
    assert r.status_code == 204
    assert client.get(f"/snippets/{sid}/").status_code == 404
    assert get_attr(mod, "Snippet").objects.filter(pk=sid).count() == 0
