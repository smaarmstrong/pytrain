"""A correct implementation of the spec in prompt.md — write tests for it."""
import warnings


class InsufficientFunds(Exception):
    pass


def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFunds(f"short by {amount - balance}")
    return balance - amount


def take(balance, amount):
    warnings.warn("take is deprecated; use withdraw", DeprecationWarning, stacklevel=2)
    return withdraw(balance, amount)
