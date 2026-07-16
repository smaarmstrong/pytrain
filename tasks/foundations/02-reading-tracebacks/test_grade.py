from pytrain_grader import load_solution, get_attr


def test_greet_no_longer_name_errors():
    greet = get_attr(load_solution(), "greet")
    assert greet("Bo") == "Hello, Bo!"
    assert greet("Ada") == "Hello, Ada!"


def test_label_age_no_longer_type_errors():
    label_age = get_attr(load_solution(), "label_age")
    assert label_age(7) == "age: 7"
    assert label_age(40) == "age: 40"


def test_last_no_longer_index_errors():
    last = get_attr(load_solution(), "last")
    assert last([3, 1, 4]) == 4
    assert last(["only"]) == "only"
    assert last([1, 2, 3, 4, 5]) == 5
