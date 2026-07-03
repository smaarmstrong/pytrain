from pytrain_grader import load_solution, get_attr


def test_track_is_a_tuple_record():
    Track = get_attr(load_solution(), "Track")
    t = Track("Hey", "Ada", 187)
    assert isinstance(t, tuple)
    assert t == ("Hey", "Ada", 187)
    assert (t.title, t.artist, t.seconds) == ("Hey", "Ada", 187)
    assert t[1] == "Ada"
    title, artist, seconds = t
    assert seconds == 187


def test_track_namedtuple_api():
    Track = get_attr(load_solution(), "Track")
    assert Track._fields == ("title", "artist", "seconds")
    t = Track(title="Hey", artist="Ada", seconds=187)
    t2 = t._replace(seconds=200)
    assert t2 == ("Hey", "Ada", 200)
    assert t.seconds == 187  # original untouched


def _cache(cap):
    return get_attr(load_solution(), "LRUCache")(cap)


def test_put_get_len():
    c = _cache(3)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    assert c.get("b") == 2
    assert c.get("zzz") is None
    assert len(c) == 2
    assert "a" in c and "zzz" not in c


def test_evicts_least_recently_used():
    c = _cache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1  # refresh "a"
    c.put("c", 3)  # evicts "b"
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3
    assert len(c) == 2


def test_put_update_refreshes_recency():
    c = _cache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)  # update refreshes "a"; no eviction
    assert len(c) == 2
    c.put("c", 3)  # evicts "b"
    assert c.get("b") is None
    assert c.get("a") == 10


def test_contains_does_not_refresh():
    c = _cache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert "a" in c  # must NOT refresh "a"
    c.put("c", 3)  # evicts "a"
    assert c.get("a") is None
    assert c.get("b") == 2


def test_keys_in_recency_order():
    c = _cache(3)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.keys() == ["a", "b", "c"]
    c.get("a")
    assert c.keys() == ["b", "c", "a"]


def test_capacity_one():
    c = _cache(1)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") is None
    assert c.get("b") == 2
    assert len(c) == 1
