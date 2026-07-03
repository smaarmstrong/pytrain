"""A correct implementation of the spec in prompt.md — write tests for it.

(The grader also runs your tests against another correct implementation
that sums in a different order — don't assert exact float equality.)
"""


def mean(xs):
    if not xs:
        raise ValueError("empty data")
    return sum(xs) / len(xs)


def variance(xs):
    if not xs:
        raise ValueError("empty data")
    n = len(xs)
    m = sum(xs) / n
    return sum(x * x for x in xs) / n - m * m


def normalize(xs):
    total = sum(xs)
    if total == 0:
        raise ValueError("cannot normalize: sum is zero")
    return [x / total for x in xs]
