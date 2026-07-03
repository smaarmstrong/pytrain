"""A correct implementation of the spec in prompt.md — write tests for it."""

_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def to_roman(n):
    if not 1 <= n <= 3999:
        raise ValueError(f"expected 1..3999, got {n}")
    out = []
    for value, symbol in _VALUES:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)
