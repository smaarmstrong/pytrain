import string

from pytrain_grader import load_solution, get_attr

ALPHABET = set(string.ascii_letters + string.digits)


# ---------------------------------------------------------------- wrap

def test_wrap_example():
    wrap = get_attr(load_solution(), "wrap")
    assert wrap("the quick brown fox jumps", 10) == ["the quick", "brown fox", "jumps"]


def test_wrap_greedy_packing():
    wrap = get_attr(load_solution(), "wrap")
    # greedy: "aa bb" fits in 5, "cc" starts the next line
    assert wrap("aa bb cc", 5) == ["aa bb", "cc"]
    # a word goes on the current line whenever it fits, even if a later
    # split would be "prettier"
    assert wrap("a b c d", 3) == ["a b", "c d"]


def test_wrap_lines_never_exceed_width_and_order_kept():
    wrap = get_attr(load_solution(), "wrap")
    words = ["alpha", "be", "gamma", "d", "epsilon", "zi", "eta"]
    out = wrap(" ".join(words), 12)
    assert isinstance(out, list)
    assert all(len(line) <= 12 for line in out)
    assert " ".join(out).split() == words  # order and words preserved


def test_wrap_single_word_and_exact_fit():
    wrap = get_attr(load_solution(), "wrap")
    assert wrap("hello", 5) == ["hello"]
    assert wrap("ab cd", 5) == ["ab cd"]  # exactly width chars fits
    assert wrap("ab cd", 4) == ["ab", "cd"]


def test_wrap_empty_and_whitespace_only():
    wrap = get_attr(load_solution(), "wrap")
    assert wrap("", 10) == []
    assert wrap("   ", 10) == []


# -------------------------------------------------------------- dedent

def test_dedent_example():
    dedent = get_attr(load_solution(), "dedent")
    assert dedent("    a\n      b\n") == "a\n  b\n"


def test_dedent_common_prefix_only():
    dedent = get_attr(load_solution(), "dedent")
    # the common prefix is two spaces; deeper indents keep the remainder
    assert dedent("  x\n    y\n  z\n") == "x\n  y\nz\n"


def test_dedent_no_common_indent_is_a_noop():
    dedent = get_attr(load_solution(), "dedent")
    text = "left\n    indented\nleft again\n"
    assert dedent(text) == text


def test_dedent_ignores_empty_lines():
    dedent = get_attr(load_solution(), "dedent")
    # the blank line must not destroy (or shrink) the common prefix
    assert dedent("    a\n\n    b\n") == "a\n\nb\n"


# -------------------------------------------------------------- render

def test_render_substitutes_known_placeholders():
    render = get_attr(load_solution(), "render")
    assert render("$greeting, $name!", {"greeting": "hi", "name": "Ada"}) == "hi, Ada!"


def test_render_braced_placeholder():
    render = get_attr(load_solution(), "render")
    assert render("${a}${b}", {"a": "x", "b": "y"}) == "xy"
    assert render("${noun}s", {"noun": "cat"}) == "cats"


def test_render_leaves_unknown_placeholders_intact():
    render = get_attr(load_solution(), "render")
    assert render("$name is ${age}", {"name": "Ada"}) == "Ada is ${age}"
    assert render("$missing entirely", {}) == "$missing entirely"


def test_render_dollar_dollar_is_literal():
    render = get_attr(load_solution(), "render")
    assert render("$$5 for $item", {"item": "tea"}) == "$5 for tea"


# --------------------------------------------------------------- token

def test_token_length_and_alphabet():
    token = get_attr(load_solution(), "token")
    for n in (1, 16, 64):
        t = token(n)
        assert isinstance(t, str)
        assert len(t) == n
        assert set(t) <= ALPHABET


def test_token_zero():
    token = get_attr(load_solution(), "token")
    assert token(0) == ""


def test_token_varies_between_calls():
    token = get_attr(load_solution(), "token")
    # 62**32 possibilities: any real randomness makes a repeat impossible
    samples = {token(32) for _ in range(5)}
    assert len(samples) == 5


def test_token_draws_from_the_whole_alphabet():
    token = get_attr(load_solution(), "token")
    # 2000 draws: the chance of missing lowercase, uppercase or digits
    # entirely is astronomically small for a uniform choice over all 62
    seen = set(token(2000))
    assert seen & set(string.ascii_lowercase)
    assert seen & set(string.ascii_uppercase)
    assert seen & set(string.digits)
