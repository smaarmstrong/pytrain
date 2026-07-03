import math

import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr

# The grader's own copy of the fixed dataset from the starter.
PRODUCTS = [
    {"id": i, "name": f"prod-{i:02d}", "category": ["dairy", "fruit", "veg"][i % 3],
     "price": round(0.5 * i, 2)}
    for i in range(1, 24)
]


def expected(category=None, max_price=None, page=1, page_size=5):
    matches = [p for p in PRODUCTS
               if (category is None or p["category"] == category)
               and (max_price is None or p["price"] <= max_price)]
    total = len(matches)
    return {
        "items": matches[(page - 1) * page_size: (page - 1) * page_size + page_size],
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": math.ceil(total / page_size),
    }


@pytest.fixture()
def client():
    mod = load_solution()
    app = get_attr(mod, "app")
    return TestClient(app)


def get(client, **params):
    return client.get("/products", params=params)


def test_defaults_first_page_of_five(client):
    r = get(client)
    assert r.status_code == 200
    assert r.json() == expected()


def test_second_page(client):
    assert get(client, page=2).json() == expected(page=2)


def test_short_last_page(client):
    body = get(client, page=5).json()
    assert body == expected(page=5)
    assert len(body["items"]) == 3  # 23 items, 5 per page


def test_page_past_the_end_is_empty_not_error(client):
    r = get(client, page=6)
    assert r.status_code == 200
    body = r.json()
    assert body["items"] == []
    assert body["total"] == 23
    assert body["pages"] == 5


def test_category_filter_changes_total_and_pages(client):
    body = get(client, category="fruit").json()
    assert body == expected(category="fruit")
    assert body["total"] == 8
    assert body["pages"] == 2


def test_category_second_page(client):
    assert get(client, category="fruit", page=2).json() == expected(category="fruit", page=2)


def test_max_price_filter(client):
    assert get(client, max_price=0.5).json() == expected(max_price=0.5)


def test_filters_combine_with_and(client):
    body = get(client, category="fruit", max_price=5.0).json()
    assert body == expected(category="fruit", max_price=5.0)
    assert body["total"] == 4


def test_no_matches_gives_zero_pages(client):
    body = get(client, category="frozen").json()
    assert body["items"] == []
    assert body["total"] == 0
    assert body["pages"] == 0


def test_page_size_changes_page_maths(client):
    assert get(client, page_size=10, page=3).json() == expected(page_size=10, page=3)


def test_original_order_preserved(client):
    ids = [p["id"] for p in get(client, page_size=20).json()["items"]]
    assert ids == list(range(1, 21))


def test_invalid_page_and_page_size_are_422(client):
    assert get(client, page=0).status_code == 422
    assert get(client, page=-3).status_code == 422
    assert get(client, page_size=0).status_code == 422
    assert get(client, page_size=21).status_code == 422
