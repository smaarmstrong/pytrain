from pytrain_grader import load_solution, get_attr


def test_receipt_line_basic():
    f = get_attr(load_solution(), "receipt_line")
    assert f("widget", 1234.5) == "widget      £1,234.50"


def test_receipt_line_short_price_right_aligned():
    f = get_attr(load_solution(), "receipt_line")
    assert f("tea", 3.5) == "tea         £    3.50"


def test_receipt_line_rounding_and_separator():
    f = get_attr(load_solution(), "receipt_line")
    assert f("van", 25000.005) == "van         £" + format(25000.005, ">8,.2f")
    assert f("pen", 0.1) == "pen         £    0.10"


def test_percent():
    f = get_attr(load_solution(), "percent")
    assert f(0.256) == "25.6%"
    assert f(1.0) == "100.0%"
    assert f(0.005) == "0.5%"


def test_debug_line_uses_repr():
    f = get_attr(load_solution(), "debug_line")
    assert f("n", 42) == "n=42"
    assert f("user", "bo") == "user='bo'"
    assert f("xs", [1, 2]) == "xs=[1, 2]"


def test_quoted_nested_quotes():
    f = get_attr(load_solution(), "quoted")
    assert f("Bo", "Ace") == 'Bo is called "Ace"'
    assert f("Ada Lovelace", "the Enchantress") == 'Ada Lovelace is called "the Enchantress"'
