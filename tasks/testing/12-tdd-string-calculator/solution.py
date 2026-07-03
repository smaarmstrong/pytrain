"""Reference implementation of the string calculator kata."""


def add(numbers):
    if not numbers:
        return 0
    if numbers.startswith("//"):
        header, _, rest = numbers.partition("\n")
        parts = rest.split(header[2:])
    else:
        parts = numbers.replace("\n", ",").split(",")
    values = [int(part) for part in parts]
    negatives = [v for v in values if v < 0]
    if negatives:
        raise ValueError("negatives not allowed: " + ", ".join(str(n) for n in negatives))
    return sum(values)
