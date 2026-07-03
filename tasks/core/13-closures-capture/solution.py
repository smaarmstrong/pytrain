def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


def make_accumulator(start=0):
    total = start

    def add(amount):
        nonlocal total
        total += amount
        return total

    return add


def make_multipliers(factors):
    def make_one(factor):
        return lambda x: x * factor

    return [make_one(f) for f in factors]
