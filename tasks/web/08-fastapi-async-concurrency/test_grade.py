import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def client():
    mod = load_solution()
    app = get_attr(mod, "app")
    # Context-managed client: one shared event loop for every request, so
    # anything that blocks the loop is visible in the timing tests.
    with TestClient(app) as c:
        yield c


def test_slow_shape(client):
    r = client.get("/slow/alpha")
    assert r.status_code == 200
    assert r.json() == {"source": "alpha", "length": 5}


def test_aggregate_shape_and_order(client):
    r = client.get("/aggregate", params={"sources": ["bb", "a", "cccc"]})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 3
    assert body["results"] == [
        {"source": "bb", "length": 2},
        {"source": "a", "length": 1},
        {"source": "cccc", "length": 4},
    ]


def test_aggregate_single_source(client):
    r = client.get("/aggregate", params={"sources": ["solo"]})
    assert r.json() == {"results": [{"source": "solo", "length": 4}], "count": 1}


def test_aggregate_requires_sources(client):
    r = client.get("/aggregate")
    assert r.status_code in (400, 422)


def test_aggregate_fetches_concurrently(client):
    # 5 sources x DELAY(0.2s): sequential awaits >= 1.0s, gather ~0.2s.
    start = time.perf_counter()
    r = client.get("/aggregate", params={"sources": ["a", "b", "c", "d", "e"]})
    elapsed = time.perf_counter() - start
    assert r.status_code == 200
    assert r.json()["count"] == 5
    assert elapsed < 0.7, (
        f"/aggregate with 5 sources took {elapsed:.2f}s — fetch the sources "
        "concurrently (asyncio.gather), not one await at a time"
    )


def test_parallel_requests_do_not_block_each_other(client):
    # 5 simultaneous /slow requests share one event loop; a blocking
    # endpoint (time.sleep) serialises them (>= 1.0s), async ~0.2s.
    names = ["one", "two", "three", "four", "five"]
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(lambda n: client.get(f"/slow/{n}"), names))
    elapsed = time.perf_counter() - start
    for name, r in zip(names, results):
        assert r.status_code == 200
        assert r.json() == {"source": name, "length": len(name)}
    assert elapsed < 0.7, (
        f"5 concurrent /slow requests took {elapsed:.2f}s — the endpoint is "
        "blocking the event loop (use `await asyncio.sleep`, never time.sleep)"
    )
