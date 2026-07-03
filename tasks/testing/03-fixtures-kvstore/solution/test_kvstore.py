import pytest

import kvstore


@pytest.fixture
def store():
    s = kvstore.connect()
    yield s
    s.close()


@pytest.fixture
def populated(store):
    store.put("colour", "teal")
    store.put("size", 42)
    return store


def test_put_then_get(store):
    store.put("k", 1)
    assert store.get("k") == 1


def test_put_overwrites(store):
    store.put("k", 1)
    store.put("k", 2)
    assert store.get("k") == 2


def test_get_missing_raises_keyerror(store):
    with pytest.raises(KeyError):
        store.get("nope")


def test_delete_existing_returns_true(populated):
    assert populated.delete("colour") is True
    with pytest.raises(KeyError):
        populated.get("colour")


def test_delete_missing_returns_false(store):
    assert store.delete("ghost") is False


def test_operations_after_close_raise(store):
    store.put("k", 1)
    store.close()
    with pytest.raises(kvstore.StoreClosed):
        store.get("k")
    with pytest.raises(kvstore.StoreClosed):
        store.put("k", 2)
    with pytest.raises(kvstore.StoreClosed):
        store.delete("k")


def test_close_is_idempotent(store):
    store.close()
    store.close()
    reopened = kvstore.connect()  # the slot must be free again
    reopened.close()
