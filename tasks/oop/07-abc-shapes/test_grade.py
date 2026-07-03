import math

import pytest

from pytrain_grader import load_solution, get_attr


def shapes():
    mod = load_solution()
    return (get_attr(mod, "Shape"), get_attr(mod, "Rectangle"),
            get_attr(mod, "Circle"))


def test_shape_cannot_be_instantiated():
    Shape, *_ = shapes()
    with pytest.raises(TypeError):
        Shape()


def test_incomplete_subclass_cannot_be_instantiated():
    Shape, *_ = shapes()

    class OnlyArea(Shape):
        def area(self):
            return 1.0

    with pytest.raises(TypeError):
        OnlyArea()

    class Nothing(Shape):
        pass

    with pytest.raises(TypeError):
        Nothing()


def test_complete_subclass_instantiates_fine():
    Shape, *_ = shapes()

    class Tri(Shape):
        def area(self):
            return 6.0

        def perimeter(self):
            return 12.0

    assert Tri().area() == 6.0


def test_rectangle_maths():
    _, Rectangle, _ = shapes()
    r = Rectangle(3, 4)
    assert r.area() == pytest.approx(12)
    assert r.perimeter() == pytest.approx(14)


def test_circle_maths():
    *_, Circle = shapes()
    c = Circle(2)
    assert c.area() == pytest.approx(4 * math.pi)
    assert c.perimeter() == pytest.approx(4 * math.pi)


def test_shapes_are_subclasses_of_shape():
    Shape, Rectangle, Circle = shapes()
    assert issubclass(Rectangle, Shape)
    assert issubclass(Circle, Shape)


def test_describe_format():
    _, Rectangle, Circle = shapes()
    assert Rectangle(3, 4).describe() == "Rectangle: area=12.00, perimeter=14.00"
    assert Circle(1).describe() == "Circle: area=3.14, perimeter=6.28"


def test_describe_is_inherited_and_uses_runtime_class():
    Shape, *_ = shapes()

    class Tri(Shape):
        def area(self):
            return 6.0

        def perimeter(self):
            return 12.0

    assert Tri().describe() == "Tri: area=6.00, perimeter=12.00"
