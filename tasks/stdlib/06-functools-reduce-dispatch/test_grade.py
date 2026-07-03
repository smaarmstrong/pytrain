from pytrain_grader import load_solution, get_attr


def test_product_of():
    f = get_attr(load_solution(), "product_of")
    assert f([2, 3, 4]) == 24
    assert f([5]) == 5
    assert f([]) == 1
    assert f([3, 0, 9]) == 0


def test_compose_identity():
    compose = get_attr(load_solution(), "compose")
    ident = compose()
    assert ident(42) == 42
    assert ident("x") == "x"


def test_compose_single_and_order():
    compose = get_attr(load_solution(), "compose")
    assert compose(str)(5) == "5"
    add1 = lambda x: x + 1  # noqa: E731
    dbl = lambda x: x * 2  # noqa: E731
    assert compose(add1, dbl)(3) == 7  # add1(dbl(3)), not dbl(add1(3)) == 8
    assert compose(dbl, add1)(3) == 8
    assert compose(str, add1, dbl)(10) == "21"


def test_describe_builtin_types():
    describe = get_attr(load_solution(), "describe")
    assert describe(5) == "int:5"
    assert describe(-3) == "int:-3"
    assert describe("hi") == "str:hi"
    assert describe([1, 2, 3]) == "list:3"
    assert describe([]) == "list:0"
    assert describe(3.5) == "other:float"
    assert describe((1, 2)) == "other:tuple"


def test_describe_register_new_type():
    describe = get_attr(load_solution(), "describe")

    class Point:
        pass

    describe.register(Point, lambda p: "a point")
    assert describe(Point()) == "a point"
    # other types keep their behaviour
    assert describe(7) == "int:7"


def test_describe_registered_handler_covers_subclasses():
    describe = get_attr(load_solution(), "describe")

    class Shape:
        pass

    class Circle(Shape):
        pass

    describe.register(Shape, lambda s: "a shape")
    assert describe(Circle()) == "a shape"
