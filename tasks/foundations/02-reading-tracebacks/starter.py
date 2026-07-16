# Three buggy functions. Run this file, read the traceback (bottom-up!),
# fix the line it points at. Repeat until all three calls work.


def greet(name):
    """greet("Bo") -> "Hello, Bo!" """
    return "Hello, " + nmae + "!"


def label_age(age):
    """label_age(7) -> "age: 7" """
    return "age: " + age


def last(items):
    """last([3, 1, 4]) -> 4 — the final element."""
    return items[len(items)]


if __name__ == "__main__":
    # Uncomment ONE call at a time, run `python3 solution.py`, read the
    # traceback, fix the function, re-run. Then move to the next.
    print(greet("Bo"))
    # print(label_age(7))
    # print(last([3, 1, 4]))
