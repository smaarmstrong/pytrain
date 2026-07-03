import subprocess
import sys

from pytrain_grader import load_solution, get_attr, workspace


def _mypy(target):
    return subprocess.run(
        [sys.executable, "-m", "mypy", "--no-error-summary", "--soft-error-limit=-1",
         "--disallow-untyped-defs", str(target)],
        capture_output=True, text=True, cwd=str(workspace()),
    )


# ---- behaviour --------------------------------------------------------------

def test_shapes_draw():
    mod = load_solution()
    Circle, Square = get_attr(mod, "Circle"), get_attr(mod, "Square")
    assert Circle(2).draw() == "circle(r=2)"
    assert Square(3).draw() == "square(s=3)"


def test_render_all_in_order():
    mod = load_solution()
    Circle, Square = get_attr(mod, "Circle"), get_attr(mod, "Square")
    render_all = get_attr(mod, "render_all")
    assert render_all([Circle(2), Square(3), Circle(5)]) \
        == ["circle(r=2)", "square(s=3)", "circle(r=5)"]
    assert render_all([]) == []


def test_render_all_accepts_any_structural_drawable():
    render_all = get_attr(load_solution(), "render_all")

    class Text:  # never seen by the learner: structural typing in action
        def draw(self) -> str:
            return "text"

    assert render_all([Text(), Text()]) == ["text", "text"]


def test_protocol_is_runtime_checkable():
    mod = load_solution()
    Drawable = get_attr(mod, "Drawable")
    Circle = get_attr(mod, "Circle")

    class Duck:
        def draw(self) -> str:
            return "duck"

    assert isinstance(Circle(1), Drawable)
    assert isinstance(Duck(), Drawable), (
        "a class with draw() must satisfy Drawable structurally"
    )
    assert not isinstance(42, Drawable)


def test_implementations_do_not_inherit_the_protocol():
    mod = load_solution()
    Drawable = get_attr(mod, "Drawable")
    for cls_name in ("Circle", "Square"):
        cls = get_attr(mod, cls_name)
        assert Drawable not in cls.__mro__, (
            f"{cls_name} must satisfy Drawable by shape, not by inheriting it"
        )


# ---- typing -----------------------------------------------------------------

def test_mypy_clean_on_module():
    proc = _mypy(workspace() / "solution.py")
    assert proc.returncode == 0, (
        "mypy is not clean under --disallow-untyped-defs:\n" + proc.stdout + proc.stderr
    )


def test_mypy_accepts_structural_implementations():
    snippet = workspace() / "_check_proto_ok.py"
    snippet.write_text(
        "from solution import Circle, Square, render_all\n"
        "\n"
        "class Text:\n"
        "    def draw(self) -> str:\n"
        '        return "text"\n'
        "\n"
        "out: list[str] = render_all([Circle(1), Square(2), Text()])\n"
    )
    proc = _mypy(snippet)
    assert proc.returncode == 0, (
        "mypy rejected structurally-valid Drawables passed to render_all:\n"
        + proc.stdout + proc.stderr
    )


def test_mypy_rejects_non_drawables():
    snippet = workspace() / "_check_proto_bad.py"
    snippet.write_text(
        "from solution import render_all\n"
        "render_all([42])\n"
    )
    proc = _mypy(snippet)
    assert proc.returncode != 0, (
        "mypy accepted render_all([42]) — render_all must be annotated to take "
        "an iterable of Drawable, not Any/object"
    )
