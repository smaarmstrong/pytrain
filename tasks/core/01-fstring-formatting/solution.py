def receipt_line(item: str, price: float) -> str:
    return f"{item:<12}£{price:>8,.2f}"


def percent(fraction: float) -> str:
    return f"{fraction:.1%}"


def debug_line(name: str, value) -> str:
    return f"{name}={value!r}"


def quoted(name: str, nickname: str) -> str:
    return f'{name} is called "{nickname}"'
