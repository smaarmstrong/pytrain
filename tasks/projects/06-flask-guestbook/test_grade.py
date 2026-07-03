"""Grades the guestbook through Flask's test_client — no server, no ports.

create_app() is called per test (and twice in the isolation test), so the
factory must build a fresh app + fresh store every time.
"""
import pytest

from pytrain_grader import load_solution, get_attr


def make_app():
    mod = load_solution(filename="app.py", module_name="guestbook_app")
    create_app = get_attr(mod, "create_app")
    return create_app()


@pytest.fixture()
def client():
    return make_app().test_client()


def post_form(client, name="Ada", message="hi"):
    return client.post("/entries/", data={"name": name, "message": message})


# -- factory + blueprint wiring ---------------------------------------------

def test_health_route(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_blueprint_module_exposes_bp(client):
    import flask

    entries = load_solution(filename="entries.py", module_name="guestbook_entries")
    bp = get_attr(entries, "bp")
    assert isinstance(bp, flask.Blueprint)


def test_each_factory_call_has_its_own_store():
    a = make_app().test_client()
    b = make_app().test_client()
    post_form(a, "OnlyInA", "secret")
    assert len(a.get("/entries/").get_json()) == 1
    assert b.get("/entries/").get_json() == []


# -- create -----------------------------------------------------------------

def test_empty_list_initially(client):
    r = client.get("/entries/")
    assert r.status_code == 200
    assert r.get_json() == []


def test_post_form_creates_entry(client):
    r = post_form(client, "Ada", "hello there")
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "name": "Ada", "message": "hello there"}


def test_post_json_creates_entry(client):
    r = client.post("/entries/", json={"name": "Grace", "message": "yo"})
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "name": "Grace", "message": "yo"}


def test_ids_increment_and_order_is_oldest_first(client):
    post_form(client, "One", "m1")
    client.post("/entries/", json={"name": "Two", "message": "m2"})
    post_form(client, "Three", "m3")
    got = client.get("/entries/").get_json()
    assert [e["id"] for e in got] == [1, 2, 3]
    assert [e["name"] for e in got] == ["One", "Two", "Three"]


def test_values_are_stripped(client):
    r = client.post("/entries/", json={"name": "  Ada  ", "message": "\thi\n"})
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "name": "Ada", "message": "hi"}


# -- validation ---------------------------------------------------------------

@pytest.mark.parametrize("payload", [
    {"name": "", "message": "x"},
    {"name": "x", "message": ""},
    {"name": "   ", "message": "x"},      # blank after stripping
    {"message": "no name"},
    {"name": "no message"},
])
def test_missing_or_blank_fields_are_400(client, payload):
    r = client.post("/entries/", json=payload)
    assert r.status_code == 400
    assert r.get_json() == {"error": "name and message are required"}
    assert client.get("/entries/").get_json() == []   # nothing stored


def test_400_form_variant_then_valid_post_still_works(client):
    r = client.post("/entries/", data={"name": "", "message": "x"})
    assert r.status_code == 400
    assert post_form(client, "Ada", "hi").status_code == 201
    assert [e["name"] for e in client.get("/entries/").get_json()] == ["Ada"]


# -- get by id ----------------------------------------------------------------

def test_get_by_id(client):
    post_form(client, "Ada", "first")
    post_form(client, "Grace", "second")
    r = client.get("/entries/2")
    assert r.status_code == 200
    assert r.get_json() == {"id": 2, "name": "Grace", "message": "second"}


def test_get_missing_is_404(client):
    r = client.get("/entries/99")
    assert r.status_code == 404
    assert r.get_json() == {"error": "not found"}
