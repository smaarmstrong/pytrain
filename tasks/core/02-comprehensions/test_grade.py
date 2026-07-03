from pytrain_grader import load_solution, get_attr


def test_squares_of_evens():
    f = get_attr(load_solution(), "squares_of_evens")
    assert f([1, 2, 3, 4]) == [4, 16]
    assert f(range(6)) == [0, 4, 16]
    assert f([1, 3, 5]) == []
    assert f([]) == []


def test_word_lengths():
    f = get_attr(load_solution(), "word_lengths")
    assert f(["Hi", "there"]) == {"hi": 2, "there": 5}
    assert f(["", "a", ""]) == {"a": 1}
    assert f([]) == {}
    assert isinstance(f(["x"]), dict)


def test_distinct_initials():
    f = get_attr(load_solution(), "distinct_initials")
    out = f(["ada", "Alan", "grace", ""])
    assert out == {"A", "G"}
    assert isinstance(out, set)
    assert f([]) == set()


def test_flatten_matrix():
    f = get_attr(load_solution(), "flatten_matrix")
    assert f([[1, 2], [3], []]) == [1, 2, 3]
    assert f([]) == []
    assert f([[], []]) == []
    assert f([["a"], ["b", "c"]]) == ["a", "b", "c"]


def test_parity_labels():
    f = get_attr(load_solution(), "parity_labels")
    assert f([1, 2]) == ["odd", "even"]
    assert f([0, 7, 8]) == ["even", "odd", "even"]
    assert f([]) == []


def test_inputs_not_mutated():
    mod = load_solution()
    nums = [1, 2, 3]
    get_attr(mod, "squares_of_evens")(nums)
    assert nums == [1, 2, 3]
    matrix = [[1], [2]]
    get_attr(mod, "flatten_matrix")(matrix)
    assert matrix == [[1], [2]]
