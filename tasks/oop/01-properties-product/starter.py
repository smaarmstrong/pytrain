class Product:
    """A product with a validated `price` property and a shared `currency`
    class attribute. See prompt.md for the full spec."""

    currency = "GBP"

    def __init__(self, name, price=0.0):
        raise NotImplementedError
