class Checkout:
    """total(prices) = subtotal minus whatever self.strategy(subtotal) says,
    rounded to 2 dp and floored at 0.0. See prompt.md."""

    def __init__(self, strategy=None):
        raise NotImplementedError

    def total(self, prices):
        raise NotImplementedError


def no_discount(subtotal):
    raise NotImplementedError


def percent_off(pct):
    """Return a strategy callable giving pct% off."""
    raise NotImplementedError


def bulk_discount(threshold, pct):
    """Return a strategy callable giving pct% off once subtotal >= threshold."""
    raise NotImplementedError
