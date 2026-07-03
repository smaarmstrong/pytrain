import flask
import pytest

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def mod():
    return load_solution()


def test_api_bp_is_a_blueprint(mod):
    bp = get_attr(mod, "api_bp")
    assert isinstance(bp, flask.Blueprint)


def test_create_app_returns_flask_app(mod):
    create_app = get_attr(mod, "create_app")
    app = create_app()
    assert isinstance(app, flask.Flask)


def test_status_default_app_name(mod):
    app = get_attr(mod, "create_app")()
    r = app.test_client().get("/api/v1/status")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok", "app_name": "default"}


def test_status_uses_config(mod):
    app = get_attr(mod, "create_app")({"APP_NAME": "shop"})
    r = app.test_client().get("/api/v1/status")
    assert r.get_json() == {"status": "ok", "app_name": "shop"}


def test_two_apps_have_independent_config(mod):
    create_app = get_attr(mod, "create_app")
    one = create_app({"APP_NAME": "one"})
    two = create_app({"APP_NAME": "two"})
    assert one.test_client().get("/api/v1/status").get_json()["app_name"] == "one"
    assert two.test_client().get("/api/v1/status").get_json()["app_name"] == "two"


def test_routes_are_prefixed(mod):
    app = get_attr(mod, "create_app")()
    # unprefixed path must not exist
    assert app.test_client().get("/status").status_code == 404
    assert app.test_client().get("/api/v1/status").status_code == 200


def test_double(mod):
    app = get_attr(mod, "create_app")()
    r = app.test_client().get("/api/v1/double/21")
    assert r.status_code == 200
    assert r.get_json() == {"result": 42}


def test_hits_counts_per_app(mod):
    create_app = get_attr(mod, "create_app")
    one = create_app()
    two = create_app()
    c1 = one.test_client()
    assert c1.post("/api/v1/hits").get_json() == {"hits": 1}
    assert c1.post("/api/v1/hits").get_json() == {"hits": 2}
    assert c1.post("/api/v1/hits").get_json() == {"hits": 3}
    # a fresh app starts from scratch — no shared module-level counter
    assert two.test_client().post("/api/v1/hits").get_json() == {"hits": 1}
