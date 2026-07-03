class Widget:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # object() raises TypeError on leftovers

    def render(self):
        return ["widget"]


class BorderMixin:
    def __init__(self, *, border="solid", **kwargs):
        super().__init__(**kwargs)
        self.border = border

    def render(self):
        return ["border"] + super().render()


class ScrollMixin:
    def __init__(self, *, scroll="vertical", **kwargs):
        super().__init__(**kwargs)
        self.scroll = scroll

    def render(self):
        return ["scroll"] + super().render()


class FancyWidget(BorderMixin, ScrollMixin, Widget):
    pass
