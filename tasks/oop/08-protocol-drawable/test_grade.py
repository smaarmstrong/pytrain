import pytest

from pytrain_grader import load_solution, get_attr


class Square:
    def draw(self):
        return "square"


class Circle:
    def draw(self):
        return "circle"


class Blob:
    pass


class RecordingShape:
    def __init__(self, log):
        self.log = log

    def draw(self):
        self.log.append("drawn")
        return "recording"


def test_isinstance_is_structural():
    Drawable = get_attr(load_solution(), "Drawable")
    assert isinstance(Square(), Drawable)
    assert isinstance(Circle(), Drawable)


def test_isinstance_false_without_draw():
    Drawable = get_attr(load_solution(), "Drawable")
    assert not isinstance(Blob(), Drawable)
    assert not isinstance(42, Drawable)
    assert not isinstance("draw", Drawable)


def test_protocol_cannot_be_instantiated():
    Drawable = get_attr(load_solution(), "Drawable")
    with pytest.raises(TypeError):
        Drawable()


def test_draw_all_returns_outputs_in_order():
    draw_all = get_attr(load_solution(), "draw_all")
    assert draw_all([Square(), Circle(), Square()]) == ["square", "circle", "square"]


def test_draw_all_empty():
    draw_all = get_attr(load_solution(), "draw_all")
    assert draw_all([]) == []


def test_draw_all_rejects_non_drawables():
    draw_all = get_attr(load_solution(), "draw_all")
    with pytest.raises(TypeError):
        draw_all([Square(), Blob()])
    with pytest.raises(TypeError):
        draw_all([42])


def test_draw_all_validates_before_drawing_anything():
    draw_all = get_attr(load_solution(), "draw_all")
    log = []
    with pytest.raises(TypeError):
        draw_all([RecordingShape(log), Blob()])
    assert log == []  # nothing was drawn before the check failed
