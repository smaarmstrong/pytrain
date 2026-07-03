from pytrain_grader import load_solution, get_attr


def card_cls():
    return get_attr(load_solution(), "Card")


def test_attributes():
    Card = card_cls()
    c = Card("A", "spades")
    assert c.rank == "A" and c.suit == "spades"


def test_repr_exact():
    Card = card_cls()
    assert repr(Card("A", "spades")) == "Card('A', 'spades')"
    assert repr(Card("10", "hearts")) == "Card('10', 'hearts')"


def test_str_exact_and_distinct_from_repr():
    Card = card_cls()
    c = Card("A", "spades")
    assert str(c) == "A of spades"
    assert f"{c}" == "A of spades"


def test_equality_by_value():
    Card = card_cls()
    assert Card("A", "spades") == Card("A", "spades")
    assert Card("A", "spades") != Card("A", "hearts")
    assert Card("A", "spades") != Card("K", "spades")


def test_foreign_types_compare_false_not_error():
    Card = card_cls()
    c = Card("A", "spades")
    assert (c == ("A", "spades")) is False
    assert (("A", "spades") == c) is False
    assert (c == "A of spades") is False
    assert c != 42


def test_hash_consistent_with_eq():
    Card = card_cls()
    a, b = Card("A", "spades"), Card("A", "spades")
    assert hash(a) == hash(b)
    assert len({a, b, Card("2", "clubs")}) == 2


def test_usable_as_dict_key():
    Card = card_cls()
    scores = {Card("Q", "hearts"): 10}
    assert scores[Card("Q", "hearts")] == 10
