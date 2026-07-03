import random

from codec import decode, encode


def test_empty_string():
    assert encode("") == []
    assert decode([]) == ""


def test_simple_examples():
    assert encode("aaab") == [("a", 3), ("b", 1)]
    assert decode([("a", 2), ("b", 1)]) == "aab"


def test_random_roundtrip_invariants():
    rng = random.Random(1234)
    for _ in range(300):
        n = rng.randint(0, 40)
        s = "".join(rng.choice("ab") for _ in range(n))
        pairs = encode(s)
        assert decode(pairs) == s, f"round-trip failed for {s!r}"
        assert all(count >= 1 for _, count in pairs), f"non-positive count for {s!r}"
        assert all(pairs[i][0] != pairs[i + 1][0] for i in range(len(pairs) - 1)), \
            f"adjacent pairs repeat a character for {s!r}"
