from pytrain_grader import load_solution, get_attr


def dispatch():
    return get_attr(load_solution(), "dispatch")


def test_quit():
    assert dispatch()(("quit",)) == "quit"


def test_move_valid():
    f = dispatch()
    assert f(("move", 3, 4)) == "move to (3, 4)"
    assert f(("move", 0, 0)) == "move to (0, 0)"


def test_move_guard_rejects_negative_and_non_int():
    f = dispatch()
    assert f(("move", -1, 4)) == "invalid move"
    assert f(("move", 3, -2)) == "invalid move"
    assert f(("move", 1.5, 2)) == "invalid move"
    assert f(("move", "3", 4)) == "invalid move"


def test_line_nested_pattern():
    f = dispatch()
    assert f(("line", (0, 0), (2, 5))) == "line from (0, 0) to (2, 5)"
    assert f(("line", (1, 2), (3, 4))) == "line from (1, 2) to (3, 4)"
    assert f(["line", [9, 9], [0, 1]]) == "line from (9, 9) to (0, 1)"


def test_mapping_pattern_with_extra_keys():
    f = dispatch()
    assert f({"action": "set", "key": "colour", "value": "red"}) == "set colour='red'"
    assert f({"action": "set", "key": "n", "value": 3, "who": "me"}) == "set n=3"


def test_generic_sequence():
    f = dispatch()
    assert f([10, 20, 30, 40]) == "sequence of 4"
    assert f(("a", "b")) == "sequence of 2"
    assert f(("line", (0, 0))) == "sequence of 2"  # not a full line command


def test_string_is_text_not_sequence():
    f = dispatch()
    assert f("hello") == "text: hello"
    assert f("ab") == "text: ab"


def test_unknown():
    f = dispatch()
    assert f(None) == "unknown"
    assert f(42) == "unknown"
    assert f(()) == "unknown"
    assert f([]) == "unknown"
    assert f({"action": "delete"}) == "unknown"
