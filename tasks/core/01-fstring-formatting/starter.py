def receipt_line(item: str, price: float) -> str:
    """item left-aligned width 12, '£', price right-aligned width 8, comma + 2dp."""
    raise NotImplementedError


def percent(fraction: float) -> str:
    """0.256 -> '25.6%'."""
    raise NotImplementedError


def debug_line(name: str, value) -> str:
    """Mimic f'{name=}': 'name=' + repr(value)."""
    raise NotImplementedError


def quoted(name: str, nickname: str) -> str:
    """'Bo is called "Ace"' — nickname in double quotes."""
    raise NotImplementedError
