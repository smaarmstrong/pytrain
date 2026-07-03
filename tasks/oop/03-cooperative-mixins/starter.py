class Widget:
    """Base widget: render() -> ["widget"]; cooperative __init__(**kwargs)."""

    def __init__(self, **kwargs):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError


class BorderMixin:
    """Keyword-only border="solid"; render() prepends "border" cooperatively."""

    def render(self):
        raise NotImplementedError


class ScrollMixin:
    """Keyword-only scroll="vertical"; render() prepends "scroll" cooperatively."""

    def render(self):
        raise NotImplementedError


class FancyWidget(BorderMixin, ScrollMixin, Widget):
    pass
