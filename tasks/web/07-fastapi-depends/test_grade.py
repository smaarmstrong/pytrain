import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def mod():
    return load_solution()  # fresh app + store per test


@pytest.fixture()
def client(mod):
    return TestClient(get_attr(mod, "app"))


def make(client, name, price):
    return client.post("/products", json={"name": name, "price": price})


def test_create_201(client):
    r = make(client, "pen", 1.5)
    assert r.status_code == 201
    assert r.json() == {"name": "pen", "price": 1.5}


def test_duplicate_409(client):
    make(client, "pen", 1.5)
    r = make(client, "pen", 2.0)
    assert r.status_code == 409
    assert r.json() == {"detail": "product exists"}


def test_validation_422(client):
    assert client.post("/products", json={"name": "x"}).status_code == 422
    assert client.post("/products", json={"name": "x", "price": "dear"}).status_code == 422


def test_list_sorted_by_name(client):
    make(client, "zebra", 3)
    make(client, "apple", 2)
    make(client, "mango", 1)
    r = client.get("/products")
    assert r.status_code == 200
    assert [p["name"] for p in r.json()] == ["apple", "mango", "zebra"]


def test_list_q_filter_case_sensitive(client):
    make(client, "Notebook", 4)
    make(client, "notepad", 2)
    make(client, "pencil", 1)
    r = client.get("/products", params={"q": "note"})
    assert [p["name"] for p in r.json()] == ["notepad"]


def test_list_limit_default_5(client):
    for i in range(8):
        make(client, f"item{i}", i)
    assert len(client.get("/products").json()) == 5
    assert len(client.get("/products", params={"limit": 2}).json()) == 2


def test_cheap_sorted_by_price(client):
    make(client, "gold", 100.0)
    make(client, "bread", 2.5)
    make(client, "milk", 1.2)
    make(client, "jam", 2.5)
    r = client.get("/products/cheap")
    assert r.status_code == 200
    assert [p["name"] for p in r.json()] == ["milk", "bread", "jam"]


def test_cheap_shares_params_dependency(client):
    make(client, "aa", 1)
    make(client, "ab", 2)
    make(client, "ba", 3)
    r = client.get("/products/cheap", params={"q": "a", "limit": 2})
    assert [p["name"] for p in r.json()] == ["aa", "ab"]


def test_store_injected_via_depends(mod):
    app = get_attr(mod, "app")
    get_store = get_attr(mod, "get_store")
    fake = {"phantom": 3.5}
    app.dependency_overrides[get_store] = lambda: fake
    try:
        client = TestClient(app)
        got = client.get("/products").json()
        assert got == [{"name": "phantom", "price": 3.5}]
        # writes go to the injected store too
        client.post("/products", json={"name": "new", "price": 1.0})
        assert fake["new"] == 1.0
        cheap = client.get("/products/cheap").json()
        assert {p["name"] for p in cheap} == {"phantom", "new"}
    finally:
        app.dependency_overrides.clear()
