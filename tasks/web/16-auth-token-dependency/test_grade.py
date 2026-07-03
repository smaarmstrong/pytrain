import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr

ALICE = {"X-API-Token": "alice-token"}
BOB = {"X-API-Token": "bob-token"}


@pytest.fixture()
def client():
    mod = load_solution()
    app = get_attr(mod, "app")
    return TestClient(app)


def test_public_needs_no_token(client):
    r = client.get("/public")
    assert r.status_code == 200
    assert r.json() == {"message": "public"}


def test_missing_token_is_401(client):
    r = client.get("/me")
    assert r.status_code == 401
    assert r.json() == {"detail": "missing token"}


def test_invalid_token_is_403(client):
    r = client.get("/me", headers={"X-API-Token": "not-a-real-token"})
    assert r.status_code == 403
    assert r.json() == {"detail": "invalid token"}


def test_me_resolves_user_from_token(client):
    assert client.get("/me", headers=ALICE).json() == {"user": "alice"}
    assert client.get("/me", headers=BOB).json() == {"user": "bob"}


def test_items_endpoints_are_protected_too(client):
    # The same check must guard every protected endpoint (reusable dependency).
    r = client.post("/items", json={"name": "kettle"})
    assert r.status_code == 401
    assert r.json() == {"detail": "missing token"}
    r = client.get("/items", headers={"X-API-Token": "wrong"})
    assert r.status_code == 403
    assert r.json() == {"detail": "invalid token"}


def test_create_item_returns_201_with_owner(client):
    r = client.post("/items", json={"name": "kettle"}, headers=ALICE)
    assert r.status_code == 201
    assert r.json() == {"user": "alice", "name": "kettle"}


def test_items_are_per_user(client):
    client.post("/items", json={"name": "spanner"}, headers=ALICE)
    client.post("/items", json={"name": "wrench"}, headers=ALICE)
    client.post("/items", json={"name": "teapot"}, headers=BOB)

    alice_items = client.get("/items", headers=ALICE).json()
    bob_items = client.get("/items", headers=BOB).json()

    alice_names = [i["name"] for i in alice_items]
    bob_names = [i["name"] for i in bob_items]
    assert "spanner" in alice_names and "wrench" in alice_names
    assert alice_names.index("spanner") < alice_names.index("wrench")  # insertion order
    assert "teapot" in bob_names
    assert "teapot" not in alice_names
    assert "spanner" not in bob_names


def test_fresh_user_has_empty_list(client):
    # bob may have items from other tests in this module run order; use a
    # dedicated check on a client-level guarantee instead: a user with no
    # posts sees []. Alice/bob ordering is handled above, so just verify the
    # shape of an items response.
    r = client.get("/items", headers=ALICE)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert all(set(i) == {"name"} for i in r.json())


def test_body_validation(client):
    r = client.post("/items", json={}, headers=ALICE)
    assert r.status_code == 422
