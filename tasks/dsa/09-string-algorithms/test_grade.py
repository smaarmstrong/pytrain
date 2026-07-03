import random

from pytrain_grader import load_solution, get_attr


def fns():
    mod = load_solution()
    return (get_attr(mod, "is_palindrome"),
            get_attr(mod, "rle_encode"),
            get_attr(mod, "rle_decode"))


# --- is_palindrome ----------------------------------------------------------

def test_palindrome_classics():
    ip, _, _ = fns()
    assert ip("A man, a plan, a canal: Panama") is True
    assert ip("race a car") is False
    assert ip("No 'x' in Nixon") is True


def test_palindrome_edges():
    ip, _, _ = fns()
    assert ip("") is True
    assert ip(".,!") is True
    assert ip("a") is True
    assert ip("ab") is False
    assert ip("Aa") is True


def test_palindrome_digits_count():
    ip, _, _ = fns()
    assert ip("1a1") is True
    assert ip("0P") is False  # '0' and 'p' are both alphanumeric, not equal


def test_palindrome_randomized():
    ip, _, _ = fns()
    rng = random.Random(42)
    for _ in range(100):
        core = "".join(rng.choice("ab1") for _ in range(rng.randrange(0, 10)))
        pal = core + rng.choice(["", "x"]) + core[::-1]
        noisy = " ,".join(pal) + "!"
        assert ip(noisy) is True
        if len(core) >= 2 and len(set(core)) > 1:
            assert ip(core + "zq" + core) is False


# --- rle encode/decode ------------------------------------------------------

def test_encode_examples():
    _, enc, _ = fns()
    assert list(enc("aaabcc")) == [("a", 3), ("b", 1), ("c", 2)]
    assert list(enc("aab")) == [("a", 2), ("b", 1)]
    assert list(enc("")) == []
    assert list(enc("z")) == [("z", 1)]


def test_encode_runs_are_maximal():
    _, enc, _ = fns()
    assert list(enc("aa a")) == [("a", 2), (" ", 1), ("a", 1)]
    out = list(enc("xxyyxx"))
    assert out == [("x", 2), ("y", 2), ("x", 2)]
    for (c1, _), (c2, _) in zip(out, out[1:]):
        assert c1 != c2


def test_decode_examples():
    _, _, dec = fns()
    assert dec([("a", 3), ("b", 1)]) == "aaab"
    assert dec([]) == ""
    assert dec([("x", 4)]) == "xxxx"


def test_round_trip_randomized():
    _, enc, dec = fns()
    rng = random.Random(42)
    for _ in range(150):
        s = "".join(rng.choice("ab c1") for _ in range(rng.randrange(0, 50)))
        pairs = list(enc(s))
        assert dec(pairs) == s
        # every run positive length, adjacent runs differ
        assert all(n >= 1 for _, n in pairs)
        assert all(a[0] != b[0] for a, b in zip(pairs, pairs[1:]))
        assert sum(n for _, n in pairs) == len(s)
