import pytest

from pytrain_grader import load_solution, get_attr


def funcs():
    mod = load_solution()
    return (get_attr(mod, "flatten"),
            get_attr(mod, "chunk_sum"),
            get_attr(mod, "stream_sums"))


def exhaust(gen):
    """Drain a generator, returning (yielded_values, return_value)."""
    out = []
    while True:
        try:
            out.append(next(gen))
        except StopIteration as e:
            return out, e.value


# ---- flatten ----------------------------------------------------------

def test_flatten_nested_lists():
    flatten, _, _ = funcs()
    assert list(flatten([1, [2, [3, 4]], 5])) == [1, 2, 3, 4, 5]


def test_flatten_handles_tuples_and_mixes():
    flatten, _, _ = funcs()
    assert list(flatten((1, (2,), [3, (4, [5])]))) == [1, 2, 3, 4, 5]


def test_flatten_strings_are_leaves():
    flatten, _, _ = funcs()
    assert list(flatten(["ab", ["cd", 5]])) == ["ab", "cd", 5]


def test_flatten_empty_and_deep():
    flatten, _, _ = funcs()
    assert list(flatten([])) == []
    assert list(flatten([[[[7]]]])) == [7]
    assert list(flatten([[], [[]], 1])) == [1]


def test_flatten_is_a_steppable_iterator():
    flatten, _, _ = funcs()
    g = flatten([1, [2]])
    assert next(iter(g)) == 1
    assert next(g) == 2
    with pytest.raises(StopIteration):
        next(g)


def test_flatten_is_lazy():
    flatten, _, _ = funcs()

    def source():
        yield 1
        yield [2, 3]
        pytest.fail("flatten consumed its input eagerly")

    g = flatten(source())  # must not consume anything yet
    assert [next(g), next(g), next(g)] == [1, 2, 3]


# ---- chunk_sum --------------------------------------------------------

def test_chunk_sum_yields_items_then_returns_total():
    _, chunk_sum, _ = funcs()
    g = chunk_sum([4, 5])
    assert next(g) == 4
    assert next(g) == 5
    with pytest.raises(StopIteration) as exc:
        next(g)
    assert exc.value.value == 9


def test_chunk_sum_empty_chunk_returns_zero():
    _, chunk_sum, _ = funcs()
    yielded, ret = exhaust(chunk_sum([]))
    assert yielded == []
    assert ret == 0


def test_chunk_sum_negative_numbers():
    _, chunk_sum, _ = funcs()
    yielded, ret = exhaust(chunk_sum([3, -5, 2]))
    assert yielded == [3, -5, 2]
    assert ret == 0


# ---- stream_sums ------------------------------------------------------

def test_stream_sums_yields_all_numbers_in_order():
    _, _, stream_sums = funcs()
    assert list(stream_sums([[1, 2], [3]])) == [1, 2, 3]


def test_stream_sums_returns_per_chunk_sums():
    _, _, stream_sums = funcs()
    yielded, ret = exhaust(stream_sums([[1, 2], [], [3, 4, 5]]))
    assert yielded == [1, 2, 3, 4, 5]
    assert ret == [3, 0, 12]


def test_stream_sums_no_chunks():
    _, _, stream_sums = funcs()
    yielded, ret = exhaust(stream_sums([]))
    assert yielded == []
    assert ret == []


def test_stream_sums_duplicate_chunks_keep_separate_totals():
    _, _, stream_sums = funcs()
    _, ret = exhaust(stream_sums([[2, 2], [2, 2]]))
    assert ret == [4, 4]
