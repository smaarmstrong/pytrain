from pytrain_grader import load_solution, get_attr


def test_parse_log_line_named_parts():
    f = get_attr(load_solution(), "parse_log_line")
    assert f("2024-03-10 ERROR disk full") == {
        "date": "2024-03-10",
        "level": "ERROR",
        "message": "disk full",
    }


def test_parse_log_line_message_keeps_spaces():
    f = get_attr(load_solution(), "parse_log_line")
    got = f("2023-12-01 INFO user alice logged in")
    assert got == {"date": "2023-12-01", "level": "INFO", "message": "user alice logged in"}


def test_parse_log_line_rejects_nonmatching():
    f = get_attr(load_solution(), "parse_log_line")
    assert f("nonsense") is None
    assert f("2024-03-10 error lowercase level") is None
    assert f("") is None


def test_find_ints():
    f = get_attr(load_solution(), "find_ints")
    assert f("t -3 x12") == [-3, 12]
    assert f("no digits here") == []
    assert f("7") == [7]
    assert f("a 42 b 7 c 42") == [42, 7, 42]


def test_int_spans_match_the_text():
    f = get_attr(load_solution(), "int_spans")
    text = "a 42 b 7"
    spans = f(text)
    assert spans == [(2, 4), (7, 8)]
    for start, end in spans:
        assert text[start:end].lstrip("-").isdigit()


def test_int_spans_empty_and_negative():
    f = get_attr(load_solution(), "int_spans")
    assert f("nothing") == []
    text = "temp -3 deg"
    (span,) = f(text)
    assert text[span[0]:span[1]] == "-3"


def test_double_ints():
    f = get_attr(load_solution(), "double_ints")
    assert f("I own 3 cats and -2 dogs") == "I own 6 cats and -4 dogs"
    assert f("scores: 10, -4") == "scores: 20, -8"


def test_double_ints_leaves_rest_untouched():
    f = get_attr(load_solution(), "double_ints")
    assert f("no numbers!") == "no numbers!"
    assert f("") == ""
    assert f("9") == "18"
    assert f("v1.2 beta 100") == "v2.4 beta 200"
