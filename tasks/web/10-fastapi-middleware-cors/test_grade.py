import pytest
from fastapi.testclient import TestClient

from pytrain_grader import load_solution, get_attr

ALLOWED = "https://app.example.com"
EVIL = "https://evil.example.com"


@pytest.fixture()
def client():
    mod = load_solution()
    return TestClient(get_attr(mod, "app"))


def test_ping(client):
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.json() == {"pong": True}


def test_teapot_status_and_headers(client):
    r = client.get("/teapot")
    assert r.status_code == 418
    assert r.json() == {"detail": "I'm a teapot"}
    assert r.headers.get("x-api-version") == "1.0"


def test_version_header_on_every_response(client):
    assert client.get("/ping").headers.get("x-api-version") == "1.0"


def test_version_header_even_on_404(client):
    r = client.get("/no/such/path")
    assert r.status_code == 404
    assert r.headers.get("x-api-version") == "1.0"


def test_request_id_echoed(client):
    r = client.get("/ping", headers={"X-Request-Id": "abc-123"})
    assert r.headers.get("x-request-id") == "abc-123"


def test_request_id_generated_when_absent(client):
    r = client.get("/ping")
    rid = r.headers.get("x-request-id")
    assert rid  # present and non-empty


def test_cors_simple_request_allowed_origin(client):
    r = client.get("/ping", headers={"Origin": ALLOWED})
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == ALLOWED


def test_cors_preflight_allowed(client):
    r = client.options(
        "/ping",
        headers={
            "Origin": ALLOWED,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Request-Id",
        },
    )
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == ALLOWED
    allowed_methods = r.headers.get("access-control-allow-methods", "")
    assert "GET" in allowed_methods
    assert "POST" in allowed_methods


def test_cors_preflight_disallowed_origin_not_granted(client):
    r = client.options(
        "/ping",
        headers={"Origin": EVIL, "Access-Control-Request-Method": "GET"},
    )
    acao = r.headers.get("access-control-allow-origin")
    assert acao not in (EVIL, "*"), "the evil origin must not be granted CORS"


def test_cors_simple_request_disallowed_origin_not_granted(client):
    r = client.get("/ping", headers={"Origin": EVIL})
    acao = r.headers.get("access-control-allow-origin")
    assert acao not in (EVIL, "*")
