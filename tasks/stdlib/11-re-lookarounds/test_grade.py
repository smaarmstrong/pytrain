from pytrain_grader import load_solution, get_attr


def test_bold_texts_lazy_not_greedy():
    f = get_attr(load_solution(), "bold_texts")
    assert f("<b>a</b> and <b>b</b>") == ["a", "b"]
    assert f("x <b>one</b> y <b>two</b> z <b>three</b>") == ["one", "two", "three"]


def test_bold_texts_edges():
    f = get_attr(load_solution(), "bold_texts")
    assert f("no tags at all") == []
    assert f("<b></b>") == [""]
    assert f("<b>only one</b>") == ["only one"]


def test_quoted_shortest_between_quotes():
    f = get_attr(load_solution(), "quoted")
    assert f('say "hi" then "bye"') == ["hi", "bye"]
    assert f('a "b" c') == ["b"]
    # greedy would return ['x" and "y'] here
    assert f('"x" and "y"') == ["x", "y"]


def test_quoted_none():
    f = get_attr(load_solution(), "quoted")
    assert f("no quotes") == []
    assert f("") == []


def test_dollar_amounts_lookbehind():
    f = get_attr(load_solution(), "dollar_amounts")
    assert f("pay $30 or 40 or $5") == [30, 5]
    assert f("$7 then 8 then $9") == [7, 9]


def test_dollar_amounts_ignores_bare_numbers():
    f = get_attr(load_solution(), "dollar_amounts")
    assert f("100 200 300") == []
    assert f("cost: $100") == [100]
    assert f("") == []


def test_split_camel():
    f = get_attr(load_solution(), "split_camel")
    assert f("camelCaseName") == "camel Case Name"
    assert f("aB") == "a B"


def test_split_camel_runs_of_capitals_kept_together():
    f = get_attr(load_solution(), "split_camel")
    assert f("parseHTTPResponse") == "parse HTTPResponse"
    assert f("simple") == "simple"
    assert f("Already Spaced") == "Already Spaced"
    assert f("") == ""
