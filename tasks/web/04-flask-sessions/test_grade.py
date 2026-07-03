import pytest

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def app():
    mod = load_solution()
    return get_attr(mod, "app")


def test_login_success(app):
    c = app.test_client()
    r = c.post("/login", json={"username": "alice", "password": "open-sesame"})
    assert r.status_code == 200
    assert r.get_json() == {"user": "alice"}


def test_login_wrong_password_401(app):
    c = app.test_client()
    r = c.post("/login", json={"username": "alice", "password": "guess"})
    assert r.status_code == 401
    assert r.get_json() == {"error": "invalid credentials"}
    # and the session is not logged in
    assert c.get("/whoami").status_code == 401


def test_login_missing_fields_401(app):
    c = app.test_client()
    assert c.post("/login", json={"username": "alice"}).status_code == 401
    assert c.post("/login", json={"password": "open-sesame"}).status_code == 401


def test_whoami_requires_login(app):
    c = app.test_client()
    r = c.get("/whoami")
    assert r.status_code == 401
    assert r.get_json() == {"error": "not logged in"}


def test_whoami_after_login_persists_across_requests(app):
    c = app.test_client()
    c.post("/login", json={"username": "bob", "password": "open-sesame"})
    r = c.get("/whoami")
    assert r.status_code == 200
    assert r.get_json() == {"user": "bob"}
    # still logged in on a later request
    assert c.get("/whoami").get_json() == {"user": "bob"}


def test_logout(app):
    c = app.test_client()
    c.post("/login", json={"username": "carol", "password": "open-sesame"})
    r = c.post("/logout")
    assert r.status_code == 200
    assert r.get_json() == {"user": None}
    assert c.get("/whoami").status_code == 401


def test_logout_when_not_logged_in_is_ok(app):
    c = app.test_client()
    r = c.post("/logout")
    assert r.status_code == 200
    assert r.get_json() == {"user": None}


def test_clients_are_independent(app):
    a = app.test_client()
    b = app.test_client()
    a.post("/login", json={"username": "alice", "password": "open-sesame"})
    assert a.get("/whoami").get_json() == {"user": "alice"}
    assert b.get("/whoami").status_code == 401


def test_visits_counts_per_session(app):
    a = app.test_client()
    b = app.test_client()
    assert a.get("/visits").get_json() == {"visits": 1}
    assert a.get("/visits").get_json() == {"visits": 2}
    assert a.get("/visits").get_json() == {"visits": 3}
    # b has its own cookie jar, so its own counter
    assert b.get("/visits").get_json() == {"visits": 1}
