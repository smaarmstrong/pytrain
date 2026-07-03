from pytrain_grader import load_solution, get_attr


def test_counter_counts():
    f = get_attr(load_solution(), "make_counter")
    c = f()
    assert (c(), c(), c()) == (1, 2, 3)


def test_counters_independent():
    f = get_attr(load_solution(), "make_counter")
    c1, c2 = f(), f()
    assert c1() == 1
    assert c1() == 2
    assert c2() == 1, "each counter must have its own state"
    assert c1() == 3
    assert c2() == 2


def test_accumulator_default_start():
    f = get_attr(load_solution(), "make_accumulator")
    acc = f()
    assert acc(5) == 5
    assert acc(-2) == 3
    assert acc(0) == 3


def test_accumulator_custom_start_and_independence():
    f = get_attr(load_solution(), "make_accumulator")
    a, b = f(100), f()
    assert a(1) == 101
    assert b(1) == 1
    assert a(2) == 103


def test_multipliers_each_capture_their_own_factor():
    f = get_attr(load_solution(), "make_multipliers")
    fs = f([2, 3, 10])
    assert [g(5) for g in fs] == [10, 15, 50], \
        "late-binding bug? every function is using the last factor"


def test_multipliers_out_of_order_and_repeated_calls():
    f = get_attr(load_solution(), "make_multipliers")
    fs = f([1, 2, 3])
    assert fs[2](2) == 6
    assert fs[0](2) == 2
    assert fs[1](2) == 4
    assert fs[1](10) == 20  # stable on repeat calls


def test_multipliers_edges():
    f = get_attr(load_solution(), "make_multipliers")
    assert f([]) == []
    fs = f([7])
    assert len(fs) == 1 and fs[0](3) == 21


def test_two_factory_calls_do_not_interfere():
    f = get_attr(load_solution(), "make_multipliers")
    first = f([2])
    second = f([100])
    assert first[0](1) == 2
    assert second[0](1) == 100
