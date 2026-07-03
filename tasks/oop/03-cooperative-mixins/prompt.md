# Cooperative mixins and the MRO

In `solution.py`, implement four classes that cooperate through `super()`:

```python
class Widget: ...
class BorderMixin: ...
class ScrollMixin: ...
class FancyWidget(BorderMixin, ScrollMixin, Widget): ...
```

Behaviour:

- `Widget()` — the base. `render()` returns `["widget"]`. Its `__init__`
  accepts `**kwargs` and passes them up cooperatively, so an unexpected
  keyword anywhere in the chain ultimately raises `TypeError`
  (e.g. `FancyWidget(bogus=1)`).
- `BorderMixin` — takes a keyword-only `border="solid"`, stores it as
  `self.border`, and forwards remaining kwargs via `super().__init__`.
  Its `render()` returns `["border"]` followed by whatever the *next class
  in the MRO* renders.
- `ScrollMixin` — same shape: keyword-only `scroll="vertical"`, stored as
  `self.scroll`; `render()` prepends `"scroll"` to the next render in the
  MRO.
- `FancyWidget(BorderMixin, ScrollMixin, Widget)` — an empty body is enough
  if the mixins cooperate properly.

The mixins must be genuinely cooperative: they may not hard-code which class
comes next. The grader also composes them in *other* orders and combinations
(e.g. `type("R", (ScrollMixin, BorderMixin, Widget), {})`) and expects the
render order to follow that class's MRO.

Examples:

```python
>>> FancyWidget().render()
['border', 'scroll', 'widget']
>>> w = FancyWidget(border="dotted", scroll="horizontal")
>>> (w.border, w.scroll)
('dotted', 'horizontal')
>>> type("R", (ScrollMixin, BorderMixin, Widget), {})().render()
['scroll', 'border', 'widget']
>>> FancyWidget(bogus=1)
TypeError: ...
```
