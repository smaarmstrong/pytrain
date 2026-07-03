class Bounded:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.name]
        except KeyError:
            raise AttributeError(self.name) from None

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number, got {type(value).__name__}")
        if not (self.minimum <= value <= self.maximum):
            raise ValueError(f"{self.name} must be in [{self.minimum}, {self.maximum}]")
        obj.__dict__[self.name] = value
