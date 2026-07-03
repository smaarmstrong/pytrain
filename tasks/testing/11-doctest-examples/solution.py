"""Temperature and text helpers — with executable docstrings."""


def c_to_f(celsius):
    """Convert a temperature from degrees Celsius to degrees Fahrenheit.

    >>> c_to_f(0)
    32.0
    >>> c_to_f(100)
    212.0
    >>> c_to_f(-40)
    -40.0
    """
    return celsius * 9 / 5 + 32


def clamp(value, lo, hi):
    """Clamp value into the inclusive range [lo, hi].

    >>> clamp(5, 0, 10)
    5
    >>> clamp(-3, 0, 10)
    0
    >>> clamp(99, 0, 10)
    10

    If lo is greater than hi, raise ValueError('lo must not exceed hi').

    >>> clamp(1, 5, 0)
    Traceback (most recent call last):
        ...
    ValueError: lo must not exceed hi
    """
    if lo > hi:
        raise ValueError("lo must not exceed hi")
    return max(lo, min(value, hi))


def initials(name):
    """Return the uppercase initials of each word, each followed by a dot.

    >>> initials('ada lovelace')
    'A.L.'
    >>> initials('grace brewster murray hopper')
    'G.B.M.H.'
    >>> initials('')
    ''
    """
    return "".join(part[0].upper() + "." for part in name.split())
