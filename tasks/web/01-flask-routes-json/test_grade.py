import pytest

from pytrain_grader import load_solution, get_attr


@pytest.fixture()
def client():
    # Fresh module load per test = fresh in-memory store.
    mod = load_solution()
    app = get_attr(mod, "app")
    return app.test_client()


def test_ping(client):
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.get_json() == {"pong": True}


def test_greet_default(client):
    r = client.get("/greet/Ada")
    assert r.status_code == 200
    assert r.get_json() == {"message": "Hello, Ada!"}


def test_greet_custom_greeting(client):
    r = client.get("/greet/Grace", query_string={"greeting": "Hi"})
    assert r.get_json() == {"message": "Hi, Grace!"}


def test_create_note_201_with_incrementing_ids(client):
    r = client.post("/notes", json={"text": "first"})
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "text": "first"}
    r2 = client.post("/notes", json={"text": "second"})
    assert r2.status_code == 201
    assert r2.get_json()["id"] == 2


def test_list_notes_insertion_order(client):
    for t in ["a", "b", "c"]:
        client.post("/notes", json={"text": t})
    r = client.get("/notes")
    assert r.status_code == 200
    assert [n["text"] for n in r.get_json()] == ["a", "b", "c"]


def test_list_notes_contains_filter(client):
    client.post("/notes", json={"text": "buy milk"})
    client.post("/notes", json={"text": "walk dog"})
    client.post("/notes", json={"text": "buy bread"})
    r = client.get("/notes", query_string={"contains": "buy"})
    assert [n["text"] for n in r.get_json()] == ["buy milk", "buy bread"]


def test_contains_is_case_sensitive(client):
    client.post("/notes", json={"text": "Buy milk"})
    r = client.get("/notes", query_string={"contains": "buy"})
    assert r.get_json() == []


def test_get_note_by_id(client):
    client.post("/notes", json={"text": "findme"})
    r = client.get("/notes/1")
    assert r.status_code == 200
    assert r.get_json() == {"id": 1, "text": "findme"}


def test_get_missing_note_404(client):
    r = client.get("/notes/999")
    assert r.status_code == 404
    assert r.get_json() == {"error": "not found"}


def test_empty_list_initially(client):
    r = client.get("/notes")
    assert r.get_json() == []
