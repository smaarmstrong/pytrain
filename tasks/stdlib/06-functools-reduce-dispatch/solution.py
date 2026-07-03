import operator
from functools import reduce, singledispatch


def product_of(nums):
    return reduce(operator.mul, nums, 1)


def compose(*funcs):
    def composed(x):
        return reduce(lambda acc, f: f(acc), reversed(funcs), x)

    return composed


@singledispatch
def describe(value):
    return f"other:{type(value).__name__}"


@describe.register
def _(value: int):
    return f"int:{value}"


@describe.register
def _(value: str):
    return f"str:{value}"


@describe.register
def _(value: list):
    return f"list:{len(value)}"
