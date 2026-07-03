from pytrain_grader import load_solution, get_attr


def test_append_item_no_shared_default_state():
    f = get_attr(load_solution(), "append_item")
    assert f(1) == [1]
    assert f(2) == [2]  # the classic mutable-default bug returns [1, 2]
    assert f(3) == [3]


def test_append_item_mutates_and_returns_given_list():
    f = get_attr(load_solution(), "append_item")
    bucket = ["a"]
    out = f("b", bucket)
    assert out is bucket
    assert bucket == ["a", "b"]


def test_next_id_counts_from_one():
    mod = load_solution()
    f = get_attr(mod, "next_id")
    assert (f(), f(), f()) == (1, 2, 3)


def test_next_id_fresh_module_restarts():
    # load_solution() re-executes the module: the global counter resets.
    f1 = get_attr(load_solution(), "next_id")
    assert f1() == 1
    f2 = get_attr(load_solution(), "next_id")
    assert f2() == 1


def test_make_prefixer_basic():
    f = get_attr(load_solution(), "make_prefixer")
    shout = f(">> ")
    assert shout("hi") == ">> hi"
    assert shout("bye") == ">> bye"


def test_make_prefixer_independent_closures():
    f = get_attr(load_solution(), "make_prefixer")
    a = f("a-")
    b = f("b-")
    assert a("x") == "a-x"
    assert b("x") == "b-x"
    assert a("y") == "a-y"  # `a` unaffected by creating `b`
