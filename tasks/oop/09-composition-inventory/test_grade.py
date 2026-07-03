import pytest

from pytrain_grader import load_solution, get_attr


def inventory_cls():
    return get_attr(load_solution(), "Inventory")


def test_not_a_list_subclass():
    Inventory = inventory_cls()
    assert not isinstance(Inventory(), list)


def test_constructor_copies_the_initial_iterable():
    Inventory = inventory_cls()
    source = ["axe", "rope"]
    inv = Inventory(source)
    source.append("intruder")
    assert list(inv) == ["axe", "rope"]
    assert "intruder" not in inv


def test_add_and_container_protocol():
    Inventory = inventory_cls()
    inv = Inventory()
    inv.add("axe")
    inv.add("rope")
    assert len(inv) == 2
    assert "axe" in inv and "rope" in inv
    assert "torch" not in inv
    assert inv[0] == "axe" and inv[1] == "rope"
    assert list(inv) == ["axe", "rope"]


def test_indexing_out_of_range_raises_indexerror():
    Inventory = inventory_cls()
    with pytest.raises(IndexError):
        Inventory(["axe"])[5]


def test_remove_first_occurrence():
    Inventory = inventory_cls()
    inv = Inventory(["axe", "rope", "axe"])
    inv.remove("axe")
    assert list(inv) == ["rope", "axe"]


def test_remove_missing_raises_valueerror():
    Inventory = inventory_cls()
    inv = Inventory(["axe"])
    with pytest.raises(ValueError):
        inv.remove("rope")


def test_history_records_successful_mutations_in_order():
    Inventory = inventory_cls()
    inv = Inventory(["axe"])          # constructor items not recorded
    inv.add("rope")
    inv.remove("axe")
    inv.add("torch")
    assert inv.history == [("add", "rope"), ("remove", "axe"), ("add", "torch")]


def test_failed_remove_records_nothing():
    Inventory = inventory_cls()
    inv = Inventory()
    inv.add("axe")
    with pytest.raises(ValueError):
        inv.remove("rope")
    assert inv.history == [("add", "axe")]


def test_empty_inventory():
    Inventory = inventory_cls()
    inv = Inventory()
    assert len(inv) == 0
    assert list(inv) == []
    assert inv.history == []
