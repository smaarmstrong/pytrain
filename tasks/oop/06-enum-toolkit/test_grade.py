import pytest

from pytrain_grader import load_solution, get_attr


def test_priority_members_and_int_behaviour():
    mod = load_solution()
    Priority = get_attr(mod, "Priority")
    assert Priority.LOW == 1
    assert Priority.MEDIUM == 2
    assert Priority.HIGH == 3
    assert Priority.HIGH > Priority.LOW
    assert Priority.HIGH > 2
    assert Priority.LOW + 1 == 2
    assert Priority(3) is Priority.HIGH


def test_priority_sorts_like_ints():
    Priority = get_attr(load_solution(), "Priority")
    unsorted = [Priority.HIGH, Priority.LOW, Priority.MEDIUM]
    assert sorted(unsorted) == [Priority.LOW, Priority.MEDIUM, Priority.HIGH]


def test_color_values_are_lowercase_names():
    Color = get_attr(load_solution(), "Color")
    assert Color.RED == "red"
    assert Color.GREEN == "green"
    assert Color.BLUE == "blue"


def test_color_is_a_strenum():
    Color = get_attr(load_solution(), "Color")
    assert str(Color.GREEN) == "green"
    assert isinstance(Color.RED, str)
    assert Color.RED.upper() == "RED"
    assert Color("blue") is Color.BLUE


def test_permission_flags_combine_and_test_membership():
    Permission = get_attr(load_solution(), "Permission")
    combo = Permission.READ | Permission.WRITE
    assert Permission.READ in combo
    assert Permission.WRITE in combo
    assert Permission.EXECUTE not in combo
    assert combo != Permission.READ


def test_permission_members_are_distinct_bits():
    Permission = get_attr(load_solution(), "Permission")
    members = [Permission.READ, Permission.WRITE, Permission.EXECUTE]
    assert len({m.value for m in members}) == 3
    all_three = Permission.READ | Permission.WRITE | Permission.EXECUTE
    for m in members:
        assert m in all_three


def test_parse_permissions_combines_case_insensitively():
    mod = load_solution()
    Permission = get_attr(mod, "Permission")
    parse = get_attr(mod, "parse_permissions")
    assert parse(["read", "WRITE"]) == Permission.READ | Permission.WRITE
    assert parse(["Execute"]) == Permission.EXECUTE


def test_parse_permissions_empty_and_unknown():
    mod = load_solution()
    Permission = get_attr(mod, "Permission")
    parse = get_attr(mod, "parse_permissions")
    assert parse([]) == Permission(0)
    with pytest.raises(ValueError):
        parse(["admin"])
    with pytest.raises(ValueError):
        parse(["read", "banana"])
