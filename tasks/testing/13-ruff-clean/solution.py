"""Receipt helpers: subtotal, discounts and a formatted summary line."""
import math


def subtotal(prices):
    total = 0
    for price in prices:
        total += price
    return total


def apply_discount(total, code):
    if code is None:
        return total
    if code == "HALF":
        return total / 2
    try:
        percent = int(code)
    except ValueError:
        return total
    return total * (100 - percent) / 100


def summary(prices, code=None):
    total = apply_discount(subtotal(prices), code)
    label = "TOTAL"
    return label + ": " + str(math.floor(total * 100) / 100)
