from slugify import slugify


def test_lowercases():
    assert slugify("Hello World") == "hello-world"


def test_spaces_and_underscores_become_single_hyphen():
    assert slugify("python_is  great") == "python-is-great"
    assert slugify("a _ b") == "a-b"


def test_punctuation_removed():
    assert slugify("rock & roll!") == "rock-roll"


def test_hyphen_runs_collapse():
    assert slugify("a --- b") == "a-b"


def test_edges_stripped():
    assert slugify("  hello  ") == "hello"
    assert slugify("-hello-") == "hello"


def test_empty_string():
    assert slugify("") == ""
