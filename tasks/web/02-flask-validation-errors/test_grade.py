import pytest

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def client():
    mod = load_solution()
    app = get_attr(mod, "app")
    return app.test_client()


def test_unknown_url_json_404(client):
    r = client.get("/no/such/page")
    assert r.status_code == 404
    assert r.get_json() == {"error": "not found", "path": "/no/such/page"}


def test_valid_item_created_201(client):
    r = client.post("/items", json={"name": "hammer", "price": 9.5})
    assert r.status_code == 201
    body = r.get_json()
    assert body == {"id": 1, "name": "hammer", "price": 9.5}


def test_ids_increment(client):
    a = client.post("/items", json={"name": "a", "price": 1}).get_json()["id"]
    b = client.post("/items", json={"name": "b", "price": 2}).get_json()["id"]
    assert b == a + 1


def test_price_zero_is_valid(client):
    r = client.post("/items", json={"name": "freebie", "price": 0})
    assert r.status_code == 201


def test_missing_name_400(client):
    r = client.post("/items", json={"price": 1})
    assert r.status_code == 400
    assert r.get_json() == {"error": "bad request", "detail": "name is required"}


def test_empty_name_400(client):
    r = client.post("/items", json={"name": "", "price": 1})
    assert r.status_code == 400
    assert r.get_json()["detail"] == "name is required"


def test_non_string_name_400(client):
    r = client.post("/items", json={"name": 42, "price": 1})
    assert r.status_code == 400
    assert r.get_json()["detail"] == "name is required"


def test_non_json_body_400_name_message(client):
    r = client.post("/items", data="not json", content_type="text/plain")
    assert r.status_code == 400
    assert r.get_json() == {"error": "bad request", "detail": "name is required"}


def test_missing_price_400(client):
    r = client.post("/items", json={"name": "x"})
    assert r.status_code == 400
    assert r.get_json() == {
        "error": "bad request",
        "detail": "price must be a non-negative number",
    }


def test_negative_price_400(client):
    r = client.post("/items", json={"name": "x", "price": -1})
    assert r.status_code == 400
    assert r.get_json()["detail"] == "price must be a non-negative number"


def test_non_numeric_price_400(client):
    r = client.post("/items", json={"name": "x", "price": "cheap"})
    assert r.status_code == 400
    assert r.get_json()["detail"] == "price must be a non-negative number"


def test_name_checked_before_price(client):
    r = client.post("/items", json={})
    assert r.status_code == 400
    assert r.get_json()["detail"] == "name is required"


def test_get_item_roundtrip(client):
    client.post("/items", json={"name": "saw", "price": 12})
    r = client.get("/items/1")
    assert r.status_code == 200
    assert r.get_json() == {"id": 1, "name": "saw", "price": 12}


def test_get_missing_item_json_404(client):
    r = client.get("/items/999")
    assert r.status_code == 404
    assert r.get_json() == {"error": "not found", "path": "/items/999"}
