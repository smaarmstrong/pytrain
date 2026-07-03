class Temperature:
    ABSOLUTE_ZERO = -273.15

    def __init__(self, celsius):
        celsius = float(celsius)
        if not self.is_valid(celsius):
            raise ValueError("below absolute zero")
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        return cls((fahrenheit - 32) * 5 / 9)

    @classmethod
    def from_string(cls, text):
        text = text.strip()
        if not text or text[-1].upper() not in ("C", "F"):
            raise ValueError(f"cannot parse {text!r}")
        try:
            value = float(text[:-1])
        except ValueError:
            raise ValueError(f"cannot parse {text!r}") from None
        if text[-1].upper() == "F":
            return cls.from_fahrenheit(value)
        return cls(value)

    @staticmethod
    def is_valid(celsius):
        return celsius >= Temperature.ABSOLUTE_ZERO
