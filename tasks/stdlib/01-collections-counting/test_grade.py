from pytrain_grader import load_solution, get_attr


def test_word_counts_basic():
    f = get_attr(load_solution(), "word_counts")
    assert dict(f("The cat saw the dog")) == {"the": 2, "cat": 1, "saw": 1, "dog": 1}


def test_word_counts_empty():
    f = get_attr(load_solution(), "word_counts")
    assert dict(f("")) == {}


def test_top_n_ties_alphabetical():
    f = get_attr(load_solution(), "top_n")
    assert f("b b a a c", 2) == [("a", 2), ("b", 2)]


def test_top_n_order_and_truncation():
    f = get_attr(load_solution(), "top_n")
    assert f("x x x y y z", 2) == [("x", 3), ("y", 2)]
    assert f("x x x y y z", 10) == [("x", 3), ("y", 2), ("z", 1)]


def test_group_by_length_preserves_order():
    f = get_attr(load_solution(), "group_by_length")
    assert f(["hi", "the", "a", "an", "cat"]) == {2: ["hi", "an"], 3: ["the", "cat"], 1: ["a"]}


def test_group_by_length_empty():
    f = get_attr(load_solution(), "group_by_length")
    assert f([]) == {}


def test_tail_basic():
    f = get_attr(load_solution(), "tail")
    assert f([1, 2, 3, 4], 2) == [3, 4]


def test_tail_short_and_zero():
    f = get_attr(load_solution(), "tail")
    assert f([1, 2], 5) == [1, 2]
    assert f([1, 2, 3], 0) == []


def test_tail_one_shot_generator():
    f = get_attr(load_solution(), "tail")
    assert f(iter(range(100_000)), 3) == [99_997, 99_998, 99_999]
