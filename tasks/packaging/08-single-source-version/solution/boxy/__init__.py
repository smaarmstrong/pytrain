"""boxy — draw boxes around text."""

__version__ = "1.2.3"


def box(text):
    line = "+" + "-" * (len(text) + 2) + "+"
    return "\n".join([line, f"| {text} |", line])
