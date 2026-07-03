"""Grades the notes API through TestClient (httpx) — no ports, no uvicorn.
main.py is re-imported per test, so each test sees a fresh store."""
import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr

KEY = {"X-API-Key": "sekrit-123"}


@pytest.fixture()
def client():
    mod = load_solution(filename="main.py", module_name="notes_main")
    app = get_attr(mod, "app")
    return TestClient(app)


def make(client, title="t", body="b", tags=None):
    payload = {"title": title, "body": body}
    if tags is not None:
        payload["tags"] = tags
    return client.post("/notes", json=payload, headers=KEY)


# -- auth ------------------------------------------------------------------

def test_missing_key_is_401(client):
    for r in (client.get("/notes"), client.post("/notes", json={"title": "t", "body": "b"})):
        assert r.status_code == 401
        assert r.json() == {"detail": "invalid API key"}


def test_wrong_key_is_401_everywhere(client):
    bad = {"X-API-Key": "letmein"}
    assert client.get("/notes", headers=bad).status_code == 401
    assert client.get("/notes/1", headers=bad).status_code == 401
    assert client.put("/notes/1", json={"title": "t", "body": "b"}, headers=bad).status_code == 401
    assert client.delete("/notes/1", headers=bad).status_code == 401


# -- create + validation ---------------------------------------------------

def test_create_returns_201_with_id_and_default_tags(client):
    r = make(client, "shopping", "milk")
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "shopping", "body": "milk", "tags": []}


def test_ids_increment(client):
    a = make(client, "one", "x").json()["id"]
    b = make(client, "two", "y").json()["id"]
    assert b == a + 1


def test_validation_422(client):
    assert make(client, title="no body is invalid", body=None).status_code == 422
    r = client.post("/notes", json={"body": "no title"}, headers=KEY)
    assert r.status_code == 422
    assert make(client, title="", body="b").status_code == 422          # empty title
    assert make(client, title="x" * 101, body="b").status_code == 422   # too long
    assert make(client, title="x" * 100, body="b").status_code == 201   # boundary ok
    assert make(client, "t", "b", tags="not-a-list").status_code == 422


# -- read ------------------------------------------------------------------

def test_get_by_id_and_404(client):
    nid = make(client, "findable", "body", ["a"]).json()["id"]
    r = client.get(f"/notes/{nid}", headers=KEY)
    assert r.status_code == 200
    assert r.json() == {"id": nid, "title": "findable", "body": "body", "tags": ["a"]}
    r = client.get("/notes/999999", headers=KEY)
    assert r.status_code == 404
    assert r.json() == {"detail": "note not found"}


def test_list_all_in_creation_order(client):
    make(client, "first", "1")
    make(client, "second", "2")
    r = client.get("/notes", headers=KEY)
    assert r.status_code == 200
    assert [n["title"] for n in r.json()] == ["first", "second"]


def test_list_filters_by_tag(client):
    make(client, "a", "x", ["home", "urgent"])
    make(client, "b", "x", ["work"])
    make(client, "c", "x", ["home"])
    r = client.get("/notes", params={"tag": "home"}, headers=KEY)
    assert {n["title"] for n in r.json()} == {"a", "c"}
    r = client.get("/notes", params={"tag": "nope"}, headers=KEY)
    assert r.json() == []


# -- update ----------------------------------------------------------------

def test_put_replaces_fully(client):
    nid = make(client, "old", "old body", ["old"]).json()["id"]
    r = client.put(f"/notes/{nid}", json={"title": "new", "body": "new body"}, headers=KEY)
    assert r.status_code == 200
    assert r.json() == {"id": nid, "title": "new", "body": "new body", "tags": []}
    # persisted
    assert client.get(f"/notes/{nid}", headers=KEY).json()["title"] == "new"


def test_put_404_and_422(client):
    r = client.put("/notes/424242", json={"title": "t", "body": "b"}, headers=KEY)
    assert r.status_code == 404
    assert r.json() == {"detail": "note not found"}
    nid = make(client).json()["id"]
    r = client.put(f"/notes/{nid}", json={"title": ""}, headers=KEY)
    assert r.status_code == 422


# -- delete ----------------------------------------------------------------

def test_delete_204_then_404(client):
    nid = make(client, "doomed", "x").json()["id"]
    r = client.delete(f"/notes/{nid}", headers=KEY)
    assert r.status_code == 204
    assert r.content == b""
    assert client.get(f"/notes/{nid}", headers=KEY).status_code == 404
    r = client.delete(f"/notes/{nid}", headers=KEY)
    assert r.status_code == 404
    assert r.json() == {"detail": "note not found"}
