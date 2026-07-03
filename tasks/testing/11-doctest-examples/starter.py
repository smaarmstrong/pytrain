"""Temperature and text helpers — add doctest examples to every docstring."""


def c_to_f(celsius):
    """Convert a temperature from degrees Celsius to degrees Fahrenheit."""
    return celsius * 9 / 5 + 32


def clamp(value, lo, hi):
    """Clamp value into the inclusive range [lo, hi].

    If lo is greater than hi, raise ValueError('lo must not exceed hi').
    """
    if lo > hi:
        raise ValueError("lo must not exceed hi")
    return max(lo, min(value, hi))


def initials(name):
    """Return the uppercase initials of each word, each followed by a dot.

    For example the name 'ada lovelace' gives 'A.L.'.
    """
    return "".join(part[0].upper() + "." for part in name.split())
