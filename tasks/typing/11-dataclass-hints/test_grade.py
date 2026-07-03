import dataclasses
import typing

from pytrain_grader import load_solution, get_attr


# Annotations here are STRINGS on purpose: raw __annotations__ would hand
# back 'int', not int — only get_type_hints resolves them.
@dataclasses.dataclass
class Reading:
    sensor: "str"
    value: "int"
    history: "list[str]" = dataclasses.field(default_factory=list)


# ---- Task dataclass ----------------------------------------------------------

def test_task_is_a_dataclass_with_defaults():
    Task = get_attr(load_solution(), "Task")
    assert dataclasses.is_dataclass(Task)
    t = Task("write docs")
    assert (t.title, t.priority, t.tags, t.done) == ("write docs", 1, [], False)
    t2 = Task("x", priority=3, tags=["a"], done=True)
    assert (t2.priority, t2.tags, t2.done) == (3, ["a"], True)


def test_task_instances_do_not_share_tags():
    Task = get_attr(load_solution(), "Task")
    a, b = Task("a"), Task("b")
    a.tags.append("urgent")
    assert b.tags == [], "tags must use default_factory=list, not a shared default"


def test_task_equality():
    Task = get_attr(load_solution(), "Task")
    assert Task("a") == Task("a")
    assert Task("a") != Task("b")


def test_task_hints_resolve():
    Task = get_attr(load_solution(), "Task")
    assert typing.get_type_hints(Task) == {
        "title": str, "priority": int, "tags": list[str], "done": bool,
    }


# ---- field_types ---------------------------------------------------------------

def test_field_types_on_task():
    mod = load_solution()
    ft = get_attr(mod, "field_types")
    Task = get_attr(mod, "Task")
    assert ft(Task) == {"title": str, "priority": int, "tags": list[str], "done": bool}


def test_field_types_resolves_string_annotations():
    ft = get_attr(load_solution(), "field_types")
    got = ft(Reading)
    assert got == {"sensor": str, "value": int, "history": list[str]}, (
        f"string annotations must be RESOLVED (use get_type_hints), got {got!r}"
    )


# ---- mismatched_fields ---------------------------------------------------------

def test_mismatched_fields_clean_instance():
    mm = get_attr(load_solution(), "mismatched_fields")
    assert mm(Reading("t1", 20)) == []


def test_mismatched_fields_reports_sorted_names():
    mm = get_attr(load_solution(), "mismatched_fields")
    assert mm(Reading(sensor=99, value="hot")) == ["sensor", "value"]
    assert mm(Reading(sensor="t1", value="hot")) == ["value"]


def test_mismatched_fields_skips_parametrised_hints():
    mm = get_attr(load_solution(), "mismatched_fields")
    # history holds the "wrong" thing, but list[str] is parametrised -> skipped
    assert mm(Reading("t1", 20, history=[1, 2])) == []


def test_mismatched_fields_uses_isinstance_semantics():
    mm = get_attr(load_solution(), "mismatched_fields")
    # bool is a subclass of int, so True is acceptable for an int field
    assert mm(Reading("t1", True)) == []


def test_mismatched_fields_on_learners_task():
    mod = load_solution()
    mm = get_attr(mod, "mismatched_fields")
    Task = get_attr(mod, "Task")
    assert mm(Task(title=123)) == ["title"]
    assert mm(Task("ok")) == []
