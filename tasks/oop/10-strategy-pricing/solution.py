def no_discount(subtotal):
    return 0


def percent_off(pct):
    def strategy(subtotal):
        return subtotal * pct / 100
    return strategy


def bulk_discount(threshold, pct):
    def strategy(subtotal):
        if subtotal >= threshold:
            return subtotal * pct / 100
        return 0
    return strategy


class Checkout:
    def __init__(self, strategy=None):
        self.strategy = strategy if strategy is not None else no_discount

    def total(self, prices):
        subtotal = sum(prices)
        discount = self.strategy(subtotal)
        return round(max(subtotal - discount, 0.0), 2)
