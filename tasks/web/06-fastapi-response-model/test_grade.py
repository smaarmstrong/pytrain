import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def client():
    mod = load_solution()  # fresh app (and store) per test
    return TestClient(get_attr(mod, "app"))


def make(client, username="u", email="u@example.com", password="pw"):
    return client.post(
        "/users", json={"username": username, "email": email, "password": password}
    )


def test_create_201_public_shape_only(client):
    r = make(client, "ada", "ada@example.com", "s3cret")
    assert r.status_code == 201
    body = r.json()
    assert body == {"id": 1, "username": "ada", "email": "ada@example.com"}
    assert "password" not in body


def test_duplicate_username_409(client):
    make(client, "ada")
    r = make(client, "ada", "other@example.com")
    assert r.status_code == 409
    assert r.json() == {"detail": "username taken"}


def test_validation_422(client):
    r = client.post("/users", json={"username": "x"})
    assert r.status_code == 422


def test_list_public_shape_in_order(client):
    make(client, "a")
    make(client, "b")
    r = client.get("/users")
    assert r.status_code == 200
    got = r.json()
    assert [u["username"] for u in got] == ["a", "b"]
    for u in got:
        assert set(u.keys()) == {"id", "username", "email"}


def test_get_by_id(client):
    uid = make(client, "grace", "g@example.com").json()["id"]
    r = client.get(f"/users/{uid}")
    assert r.status_code == 200
    assert r.json() == {"id": uid, "username": "grace", "email": "g@example.com"}


def test_get_missing_404(client):
    r = client.get("/users/12345")
    assert r.status_code == 404
    assert r.json() == {"detail": "user not found"}


def test_delete_204_empty_body(client):
    uid = make(client, "gone").json()["id"]
    r = client.delete(f"/users/{uid}")
    assert r.status_code == 204
    assert r.content == b""
    assert client.get(f"/users/{uid}").status_code == 404


def test_delete_twice_404(client):
    uid = make(client, "twice").json()["id"]
    assert client.delete(f"/users/{uid}").status_code == 204
    r = client.delete(f"/users/{uid}")
    assert r.status_code == 404
    assert r.json() == {"detail": "user not found"}


def test_username_free_after_delete(client):
    uid = make(client, "recycle").json()["id"]
    client.delete(f"/users/{uid}")
    assert make(client, "recycle").status_code == 201
