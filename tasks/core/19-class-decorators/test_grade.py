from pytrain_grader import load_solution, get_attr


def decorators():
    mod = load_solution()
    return get_attr(mod, "add_repr"), get_attr(mod, "singleton")


# ---- add_repr ---------------------------------------------------------

def test_repr_lists_attributes_in_assignment_order():
    add_repr, _ = decorators()

    @add_repr
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    assert repr(Point(1, 2)) == "Point(x=1, y=2)"


def test_repr_uses_repr_of_values():
    add_repr, _ = decorators()

    @add_repr
    class Tag:
        def __init__(self, name):
            self.name = name

    assert repr(Tag("hi")) == "Tag(name='hi')"


def test_repr_of_attributeless_instance():
    add_repr, _ = decorators()

    @add_repr
    class Empty:
        pass

    assert repr(Empty()) == "Empty()"


def test_add_repr_returns_the_class_and_preserves_behaviour():
    add_repr, _ = decorators()

    @add_repr
    class Box:
        limit = 10  # class attribute must survive

        def __init__(self, n):
            self.n = n

        def double(self):
            return self.n * 2

    b = Box(4)
    assert isinstance(b, Box)
    assert b.double() == 8
    assert Box.limit == 10
    assert repr(b) == "Box(n=4)"


# ---- singleton --------------------------------------------------------

def test_every_call_returns_the_same_object():
    _, singleton = decorators()

    @singleton
    class Config:
        def __init__(self, env="dev"):
            self.env = env

    a = Config("prod")
    b = Config("ignored")
    assert a is b
    assert a.env == "prod"


def test_instance_is_of_the_original_class():
    _, singleton = decorators()

    class Base:
        pass

    Single = singleton(Base)
    obj = Single()
    assert isinstance(obj, Base)
    assert obj is Single()


def test_lazy_and_initialised_exactly_once():
    _, singleton = decorators()
    inits = []

    @singleton
    class Tracker:
        def __init__(self):
            inits.append(1)

    assert inits == [], "decoration alone must not instantiate the class"
    Tracker()
    Tracker()
    Tracker()
    assert inits == [1], "__init__ must run exactly once"


def test_first_call_arguments_are_used():
    _, singleton = decorators()

    @singleton
    class Db:
        def __init__(self, host, port=5432):
            self.host = host
            self.port = port

    d = Db("localhost", port=6543)
    assert (d.host, d.port) == ("localhost", 6543)


def test_two_singleton_classes_are_independent():
    _, singleton = decorators()

    @singleton
    class A:
        pass

    @singleton
    class B:
        pass

    a, b = A(), B()
    assert a is not b
    assert a is A() and b is B()
