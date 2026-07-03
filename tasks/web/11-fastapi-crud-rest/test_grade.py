import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def client():
    mod = load_solution()  # fresh app + store per test
    return TestClient(get_attr(mod, "app"))


def make(client, title="t", done=None):
    body = {"title": title}
    if done is not None:
        body["done"] = done
    return client.post("/tasks", json=body)


def test_create_defaults_done_false(client):
    r = make(client, "write docs")
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "write docs", "done": False}


def test_create_explicit_done(client):
    r = make(client, "done already", done=True)
    assert r.json()["done"] is True


def test_create_requires_title(client):
    assert client.post("/tasks", json={"done": True}).status_code == 422


def test_list_in_creation_order(client):
    for t in ["a", "b", "c"]:
        make(client, t)
    r = client.get("/tasks")
    assert r.status_code == 200
    assert [t["title"] for t in r.json()] == ["a", "b", "c"]


def test_list_filter_by_done(client):
    make(client, "open1")
    make(client, "closed", done=True)
    make(client, "open2")
    done = client.get("/tasks", params={"done": "true"}).json()
    assert [t["title"] for t in done] == ["closed"]
    open_ = client.get("/tasks", params={"done": "false"}).json()
    assert [t["title"] for t in open_] == ["open1", "open2"]


def test_get_detail(client):
    tid = make(client, "findme").json()["id"]
    r = client.get(f"/tasks/{tid}")
    assert r.status_code == 200
    assert r.json() == {"id": tid, "title": "findme", "done": False}


def test_get_missing_404(client):
    r = client.get("/tasks/999")
    assert r.status_code == 404
    assert r.json() == {"detail": "task not found"}


def test_put_replaces(client):
    tid = make(client, "old").json()["id"]
    r = client.put(f"/tasks/{tid}", json={"title": "new", "done": True})
    assert r.status_code == 200
    assert r.json() == {"id": tid, "title": "new", "done": True}
    assert client.get(f"/tasks/{tid}").json()["title"] == "new"


def test_put_requires_title(client):
    tid = make(client, "x").json()["id"]
    assert client.put(f"/tasks/{tid}", json={"done": True}).status_code == 422


def test_put_missing_404(client):
    r = client.put("/tasks/999", json={"title": "x", "done": False})
    assert r.status_code == 404


def test_patch_partial_title(client):
    tid = make(client, "old", done=True).json()["id"]
    r = client.patch(f"/tasks/{tid}", json={"title": "renamed"})
    assert r.status_code == 200
    assert r.json() == {"id": tid, "title": "renamed", "done": True}


def test_patch_partial_done(client):
    tid = make(client, "keep-title").json()["id"]
    r = client.patch(f"/tasks/{tid}", json={"done": True})
    assert r.json() == {"id": tid, "title": "keep-title", "done": True}


def test_patch_empty_body_changes_nothing(client):
    tid = make(client, "same").json()["id"]
    r = client.patch(f"/tasks/{tid}", json={})
    assert r.status_code == 200
    assert r.json() == {"id": tid, "title": "same", "done": False}


def test_patch_missing_404(client):
    assert client.patch("/tasks/999", json={"done": True}).status_code == 404


def test_delete_204_then_404(client):
    tid = make(client, "gone").json()["id"]
    r = client.delete(f"/tasks/{tid}")
    assert r.status_code == 204
    assert r.content == b""
    assert client.get(f"/tasks/{tid}").status_code == 404
    assert client.delete(f"/tasks/{tid}").status_code == 404


def test_ids_never_reused(client):
    a = make(client, "a").json()["id"]
    client.delete(f"/tasks/{a}")
    b = make(client, "b").json()["id"]
    assert b == a + 1
