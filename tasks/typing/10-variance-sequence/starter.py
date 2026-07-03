from collections.abc import Sequence
from typing import Generic, TypeVar

# TODO: a covariant TypeVar and a generic, covariant Box


class Box:
    def __init__(self, value):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


def total(nums):
    raise NotImplementedError


def labels_upper(labels):
    raise NotImplementedError
