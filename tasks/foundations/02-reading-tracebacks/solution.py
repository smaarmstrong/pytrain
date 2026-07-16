def greet(name):
    """greet("Bo") -> "Hello, Bo!" """
    return "Hello, " + name + "!"


def label_age(age):
    """label_age(7) -> "age: 7" """
    return "age: " + str(age)


def last(items):
    """last([3, 1, 4]) -> 4 — the final element."""
    return items[len(items) - 1]


if __name__ == "__main__":
    print(greet("Bo"))
    print(label_age(7))
    print(last([3, 1, 4]))
