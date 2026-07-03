from pytrain_grader import load_solution, get_attr, time_limited


def test_cached_returns_correct_results():
    make_cached = get_attr(load_solution(), "make_cached")
    f = make_cached(lambda x: 2 * x)
    assert f(21) == 42
    assert f(0) == 0


def test_underlying_function_called_once_per_args():
    make_cached = get_attr(load_solution(), "make_cached")
    calls = []

    def probe(x):
        calls.append(x)
        return x * x

    p = make_cached(probe)
    assert [p(3), p(3), p(3)] == [9, 9, 9]
    assert calls == [3]
    assert p(4) == 16
    assert calls == [3, 4]
    assert p(3) == 9
    assert calls == [3, 4]


def test_multiple_positional_args():
    make_cached = get_attr(load_solution(), "make_cached")
    calls = []

    def probe(a, b):
        calls.append((a, b))
        return a + b

    p = make_cached(probe)
    assert p(1, 2) == 3
    assert p(1, 2) == 3
    assert p(2, 1) == 3  # different arg tuple -> a real call
    assert calls == [(1, 2), (2, 1)]


def test_wrappers_are_independent():
    make_cached = get_attr(load_solution(), "make_cached")
    a_calls, b_calls = [], []

    def fa(x):
        a_calls.append(x)
        return x + 1

    def fb(x):
        b_calls.append(x)
        return x - 1

    ca, cb = make_cached(fa), make_cached(fb)
    assert ca(5) == 6 and cb(5) == 4
    assert a_calls == [5] and b_calls == [5]


def test_int_parser():
    int_parser = get_attr(load_solution(), "int_parser")
    assert int_parser(16)("ff") == 255
    assert int_parser(2)("101") == 5
    assert int_parser(10)("42") == 42


def test_fib_small_values():
    fib = get_attr(load_solution(), "fib")
    assert [fib(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_fib_large_is_fast():
    fib = get_attr(load_solution(), "fib")
    assert time_limited(fib, 200, seconds=5.0) == 280571172992510140037611932413038677189525
