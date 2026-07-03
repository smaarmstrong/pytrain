import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def client():
    mod = load_solution()
    return TestClient(get_attr(mod, "app"))


def order(items=None, coupon=None, name="Ada", email="ada@example.com"):
    body = {
        "customer": {"name": name, "email": email},
        "items": items if items is not None
        else [{"sku": "pen-1", "qty": 3, "unit_price": 2.0}],
    }
    if coupon is not None:
        body["coupon"] = coupon
    return body


def test_valid_order_201(client):
    r = client.post("/orders", json=order())
    assert r.status_code == 201
    assert r.json() == {"customer": "Ada", "skus": ["PEN-1"], "total": 6.0}


def test_sku_uppercased_in_order(client):
    items = [
        {"sku": "abc", "qty": 1, "unit_price": 1.0},
        {"sku": "XyZ-9", "qty": 1, "unit_price": 1.0},
    ]
    r = client.post("/orders", json=order(items=items))
    assert r.json()["skus"] == ["ABC", "XYZ-9"]


def test_total_sums_items(client):
    items = [
        {"sku": "a", "qty": 2, "unit_price": 1.5},
        {"sku": "b", "qty": 1, "unit_price": 0.4},
    ]
    r = client.post("/orders", json=order(items=items))
    assert r.json()["total"] == 3.4


def test_coupon_save10(client):
    r = client.post("/orders", json=order(coupon="SAVE10"))
    assert r.status_code == 201
    assert r.json()["total"] == 5.4


def test_coupon_save20(client):
    r = client.post("/orders", json=order(coupon="SAVE20"))
    assert r.json()["total"] == 4.8


def test_unknown_coupon_422(client):
    assert client.post("/orders", json=order(coupon="HACK")).status_code == 422


def test_empty_items_422(client):
    assert client.post("/orders", json=order(items=[])).status_code == 422


def test_email_without_at_422(client):
    assert client.post("/orders", json=order(email="not-an-email")).status_code == 422


def test_empty_customer_name_422(client):
    assert client.post("/orders", json=order(name="")).status_code == 422


def test_qty_zero_422(client):
    items = [{"sku": "a", "qty": 0, "unit_price": 1.0}]
    assert client.post("/orders", json=order(items=items)).status_code == 422


def test_free_item_422(client):
    items = [{"sku": "a", "qty": 1, "unit_price": 0}]
    assert client.post("/orders", json=order(items=items)).status_code == 422


def test_empty_sku_422(client):
    items = [{"sku": "", "qty": 1, "unit_price": 1.0}]
    assert client.post("/orders", json=order(items=items)).status_code == 422


def test_missing_nested_field_422(client):
    body = {"customer": {"name": "Ada"}, "items": [{"sku": "a", "qty": 1, "unit_price": 1.0}]}
    assert client.post("/orders", json=body).status_code == 422
