import datetime
import json

from pytrain_grader import load_solution, get_attr


def roundtrip(obj):
    mod = load_solution()
    return get_attr(mod, "from_json")(get_attr(mod, "to_json")(obj))


def test_plain_data_roundtrips_and_stays_plain():
    obj = {"a": [1, 2.5, "x", True, None], "b": {"nested": []}}
    assert roundtrip(obj) == obj


def test_to_json_is_valid_json():
    to_json = get_attr(load_solution(), "to_json")
    s = to_json({"n": 1, "tags": {"a"}, "d": datetime.date(2024, 1, 2)})
    assert isinstance(s, str)
    json.loads(s)  # must not raise


def test_plain_json_readable_by_any_consumer():
    to_json = get_attr(load_solution(), "to_json")
    assert json.loads(to_json({"a": [1, 2]})) == {"a": [1, 2]}


def test_set_roundtrip_preserves_type():
    got = roundtrip({"tags": {"py", "web", "db"}})
    assert isinstance(got["tags"], set)
    assert got["tags"] == {"py", "web", "db"}


def test_date_roundtrip_preserves_type():
    d = datetime.date(2021, 9, 1)
    got = roundtrip({"since": d})
    assert isinstance(got["since"], datetime.date)
    assert got["since"] == d


def test_nested_specials_roundtrip():
    obj = {
        "name": "core",
        "members": [
            {"name": "ada", "langs": {"py"}, "joined": datetime.date(2020, 2, 29)},
            {"name": "bob", "langs": set(), "joined": datetime.date(2023, 12, 31)},
        ],
        "empty": [],
    }
    assert roundtrip(obj) == obj


def test_empty_set_and_top_level_specials():
    got = roundtrip(set())
    assert isinstance(got, set) and got == set()
    assert roundtrip(datetime.date(1999, 1, 1)) == datetime.date(1999, 1, 1)


def test_save_and_load_files(tmp_path):
    mod = load_solution()
    save = get_attr(mod, "save")
    load_fn = get_attr(mod, "load")
    obj = {"tags": {"a", "b"}, "when": datetime.date(2024, 6, 1), "n": 3}
    p = tmp_path / "data.json"
    save(obj, p)
    assert p.exists()
    json.loads(p.read_text(encoding="utf-8"))  # file holds valid JSON
    assert load_fn(p) == obj
