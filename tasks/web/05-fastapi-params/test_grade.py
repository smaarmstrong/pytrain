import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def client():
    # Fresh import per test would re-run module state; one app per session is
    # fine because tests create disjoint data and check relative behaviour.
    mod = load_solution()
    app = get_attr(mod, "app")
    return TestClient(app)


def make(client, title="T", author="A", year=2000):
    return client.post("/books", json={"title": title, "author": author, "year": year})


def test_create_returns_201_with_id(client):
    r = make(client, "Fluent Python", "Ramalho", 2022)
    assert r.status_code == 201
    body = r.json()
    assert isinstance(body.get("id"), int)
    assert body["title"] == "Fluent Python"
    assert body["author"] == "Ramalho"
    assert body["year"] == 2022


def test_ids_increment(client):
    a = make(client, "One").json()["id"]
    b = make(client, "Two").json()["id"]
    assert b == a + 1


def test_validation_rejects_bad_body(client):
    r = client.post("/books", json={"title": "no author or year"})
    assert r.status_code == 422
    r = client.post("/books", json={"title": "x", "author": "y", "year": "not-a-year"})
    assert r.status_code == 422


def test_get_by_id(client):
    bid = make(client, "Findable", "Someone", 1999).json()["id"]
    r = client.get(f"/books/{bid}")
    assert r.status_code == 200
    assert r.json()["title"] == "Findable"


def test_404_for_missing(client):
    r = client.get("/books/999999")
    assert r.status_code == 404
    assert r.json() == {"detail": "book not found"}


def test_list_filters_by_author(client):
    make(client, "A1", "FilterMe", 2001)
    make(client, "A2", "FilterMe", 2002)
    make(client, "B1", "SomeoneElse", 2003)
    r = client.get("/books", params={"author": "FilterMe"})
    assert r.status_code == 200
    got = r.json()
    assert {b["title"] for b in got} == {"A1", "A2"}
    assert all(b["author"] == "FilterMe" for b in got)


def test_list_respects_limit(client):
    for i in range(12):
        make(client, f"L{i}", "Bulk", 2000 + i)
    r = client.get("/books", params={"author": "Bulk", "limit": 3})
    assert len(r.json()) == 3
    r = client.get("/books", params={"author": "Bulk"})
    assert len(r.json()) == 10  # default limit
