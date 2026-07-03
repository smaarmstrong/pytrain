class Product:
    currency = "GBP"

    def __init__(self, name, price=0.0):
        self.name = name
        self.price = price  # validated by the setter

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = float(value)

    @price.deleter
    def price(self):
        self._price = 0.0
