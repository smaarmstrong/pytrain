import pytest

from pytrain_grader import load_solution, get_attr


def classes():
    mod = load_solution()
    return (get_attr(mod, "Widget"), get_attr(mod, "BorderMixin"),
            get_attr(mod, "ScrollMixin"), get_attr(mod, "FancyWidget"))


def test_widget_alone():
    Widget, *_ = classes()
    assert Widget().render() == ["widget"]


def test_fancy_render_follows_mro():
    *_, FancyWidget = classes()
    assert FancyWidget().render() == ["border", "scroll", "widget"]


def test_defaults_stored():
    *_, FancyWidget = classes()
    w = FancyWidget()
    assert w.border == "solid"
    assert w.scroll == "vertical"


def test_kwargs_route_to_the_right_mixin():
    *_, FancyWidget = classes()
    w = FancyWidget(border="dotted", scroll="horizontal")
    assert w.border == "dotted"
    assert w.scroll == "horizontal"


def test_reordered_bases_change_render_order():
    Widget, BorderMixin, ScrollMixin, _ = classes()
    R = type("R", (ScrollMixin, BorderMixin, Widget), {})
    r = R(border="thin")
    assert r.render() == ["scroll", "border", "widget"]
    assert r.border == "thin"
    assert r.scroll == "vertical"


def test_single_mixin_combination_works():
    Widget, BorderMixin, _, _ = classes()
    B = type("B", (BorderMixin, Widget), {})
    assert B().render() == ["border", "widget"]
    assert B(border="double").border == "double"


def test_unexpected_kwarg_raises_typeerror():
    *_, FancyWidget = classes()
    with pytest.raises(TypeError):
        FancyWidget(bogus=1)
